import datetime
try:
    from mock import MagicMock, patch

except ImportError:
    from unittest.mock import MagicMock, patch
import sys

sys.modules['Foundation'] = MagicMock()

from middleware_s3 import s3_auth_headers

@patch("middleware_s3.ACCESS_KEY", "asdfasdf")
@patch("middleware_s3.SECRET_KEY", "asdfasdf")
@patch("middleware_s3.REGION", "us-east-1")
@patch("middleware_s3.S3_ENDPOINT", "asdfasdf")
@patch("middleware_s3.datetime")
def test_s3_auth_headers(datetime_mock, *args):
    datetime_mock.datetime.utcnow.return_value = datetime.datetime(2019, 11, 1, 18, 20, 48, 963798)
    signed_headers = {
        'x-amz-content-sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        'Authorization': 'AWS4-HMAC-SHA256 Credential=asdfasdf/20191101/us-east-1/s3/aws4_request, SignedHeaders=host;x-amz-date, Signature=c9116b1ae100793f683b0009379bc96f1b602bae2b7e86f4f68a9869b2ea51eb',
        'x-amz-date': '20191101T182048Z'
    }
    assert s3_auth_headers('http://test.com/test') == signed_headers