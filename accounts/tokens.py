from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.is_active)
        )


token_generator = EmailActivationTokenGenerator()
