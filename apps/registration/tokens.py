from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.conf import settings
from django.utils.http import base36_to_int

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
        
    def check_if_token_expired(self, token):
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if (self._num_seconds(self._now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
            return True
        return False
        
account_activation_token = AccountActivationTokenGenerator()   