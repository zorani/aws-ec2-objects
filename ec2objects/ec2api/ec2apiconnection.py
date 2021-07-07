from cloudapi import BaseRESTAPI
import sys, os, base64, datetime, hashlib, hmac
from ..ec2common.ec2exceptions import APIKeys, HostEndpoint, RequestType, ParamNotFound
from urllib.parse import urlencode
import requests


class EC2ApiConnection(BaseRESTAPI):
    def __init__(self):
        BaseRESTAPI.__init__(
            self,
            baseurl="https://ec2.amazonaws.com",
            callrateperhour=5000,
            # geometric_delay_multiplier=2,
            # maximum_geometric_delay_multiplications=6,
            # maximum_failed_attempts=3,
            geometric_delay_multiplier=1,
            maximum_geometric_delay_multiplications=1,
            maximum_failed_attempts=1,
        )
        self.service = "ec2"
        self.host = "ec2.amazonaws.com"
        # self.baseurl = "https://ec2.amazonaws.com"

        if "AWS_ACCESS_KEY_ID" in os.environ:
            # print("Token found...")
            self.access_key = os.getenv("AWS_ACCESS_KEY_ID", "")
        else:
            raise Exception('"AWS_ACCESS_KEY_ID" ENV Variable not set.')

        if "AWS_SECRET_ACCESS_KEY" in os.environ:
            # print("Token found...")
            self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "")
        else:
            raise Exception('"AWS_SECRET_ACCESS_KEY" ENV Variable not set.')

        if "AWS_DEFAULT_REGION" in os.environ:
            # print("Token found...")
            self.default_region = os.getenv("AWS_DEFAULT_REGION", "")
        else:
            raise Exception('"AWS_DEFAULT_REGION" ENV Variable not set.')

        if self.access_key is None or self.secret_key is None:
            raise APIKeys(
                "No amazon access or secret key is available, please check usage notes to export to env"
            )

        self.headers = {
            "Content-Type": "application/json",
        }

        self.sigversionfoursigning = SigVersionFourSigning()

    def get_request(self, **kwargs):
        input_params = kwargs["params"]
        # API version can be found at the following location for a service.
        # https://docs.aws.amazon.com/AWSEC2/latest/APIReference/ec2-api.pdf
        input_params["Version"] = "2016-11-15"
        # input_params["Version"] = "2021-01-01"
        region, request_parameters = self.sigversionfoursigning.splitparams(
            input_params
        )
        # Host must not include https://
        headers, canonical_querystring = self.sigversionfoursigning.dosigfour(
            self.secret_key,
            self.access_key,
            "GET",
            self.service,
            self.host,
            region,
            request_parameters,
        )
        response = super().get_request("", params=request_parameters, headers=headers)

        return response

    def post_request(self, endpoint, **kwargs):
        raise RequestType("Only GET allowed, get_request()")

    def put_request(self, endpoint, **kwargs):
        raise RequestType("Only GET allowed, get_request()")

    def delete_request(self, endpoint, **kwargs):
        raise RequestType("Only GET allowed, get_request()")

    def head_request(self, endpoint, **kwargs):
        raise RequestType("Only GET allowed, get_request()")

    def options_request(self, endpoint, **kwargs):
        raise RequestType("Only GET allowed, get_request()")


class SigVersionFourSigning:
    def __init__(self):
        self.algorithm = "AWS4-HMAC-SHA256"
        pass

    def splitparams(self, params):

        if "Region" in params:
            region = params.pop("Region")
        else:
            raise ParamNotFound("'Region' missing from request parameter")

        sortedkeys = sorted(params, key=str.lower)

        outputparams = {}
        for key in sortedkeys:
            outputparams[key] = params[key]

        return region, outputparams

    def sign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.sign(("AWS4" + key).encode("utf-8"), dateStamp)
        kRegion = self.sign(kDate, regionName)
        kService = self.sign(kRegion, serviceName)
        kSigning = self.sign(kService, "aws4_request")
        return kSigning

    def dosigfour(
        self, secret_key, access_key, method, service, host, region, orequest_parameters
    ):
        request_parameters = urlencode(orequest_parameters)
        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amzdate = t.strftime("%Y%m%dT%H%M%SZ")
        datestamp = t.strftime("%Y%m%d")  # Date w/o time, used in credential scope

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        # Step 1 is to define the verb (GET, POST, etc.)--already done.

        # Step 2: Create canonical URI--the part of the URI from domain to query
        # string (use '/' if no path)
        canonical_uri = "/"

        # Step 3: Create the canonical query string. In this example (a GET request),
        # request parameters are in the query string. Query string values must
        # be URL-encoded (space=%20). The parameters must be sorted by name.
        # For this example, the query string is pre-formatted in the request_parameters variable.
        canonical_querystring = request_parameters

        # Step 4: Create the canonical headers and signed headers. Header names
        # must be trimmed and lowercase, and sorted in code point order from
        # low to high. Note that there is a trailing \n.
        canonical_headers = "host:" + host + "\n" + "x-amz-date:" + amzdate + "\n"

        # Step 5: Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the
        # hash of the request. "Host" and "x-amz-date" are always required.
        signed_headers = "host;x-amz-date"

        # Step 6: Create payload hash (hash of the request body content). For GET
        # requests, the payload is an empty string ("").
        payload_hash = hashlib.sha256(("").encode("utf-8")).hexdigest()

        # Step 7: Combine elements to create canonical request
        canonical_request = (
            method
            + "\n"
            + canonical_uri
            + "\n"
            + canonical_querystring
            + "\n"
            + canonical_headers
            + "\n"
            + signed_headers
            + "\n"
            + payload_hash
        )

        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = "AWS4-HMAC-SHA256"
        credential_scope = (
            datestamp + "/" + region + "/" + service + "/" + "aws4_request"
        )
        string_to_sign = (
            algorithm
            + "\n"
            + amzdate
            + "\n"
            + credential_scope
            + "\n"
            + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        )

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signing_key = self.getSignatureKey(secret_key, datestamp, region, service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(
            signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256
        ).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        # The signing information can be either in a query string value or in
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        authorization_header = (
            algorithm
            + " "
            + "Credential="
            + access_key
            + "/"
            + credential_scope
            + ", "
            + "SignedHeaders="
            + signed_headers
            + ", "
            + "Signature="
            + signature
        )

        # The request can include any headers, but MUST include "host", "x-amz-date",
        # and (for this scenario) "Authorization". "host" and "x-amz-date" must
        # be included in the canonical_headers and signed_headers, as noted
        # earlier. Order here is not significant.
        # Python note: The 'host' header is added automatically by the Python 'requests' library.
        headers = {"x-amz-date": amzdate, "Authorization": authorization_header}

        return headers, canonical_querystring
