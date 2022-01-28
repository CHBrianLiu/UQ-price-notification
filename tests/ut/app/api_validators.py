import unittest

from src.app import api_validators


class TestIsWebhookSignatureValid(unittest.TestCase):
    def test_is_webhook_signature_valid_should_return_false_when_signature_is_invalid(self):
        request_body = "{}"
        channel_secret = "secret"
        signature = "wrong_signature"

        result = api_validators.is_webhook_signature_valid(request_body, channel_secret, signature)
        self.assertEqual(False, result)

    def test_is_webhook_signature_valid_should_return_true_when_signature_is_valid(self):
        request_body = "{}"
        channel_secret = "secret"
        signature = "dzJZAsrKgS3CWXM6rNBGtzgXNyx3e42VtAJkdHRRbhM="

        result = api_validators.is_webhook_signature_valid(request_body, channel_secret, signature)
        self.assertEqual(True, result)
