from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

DEFAULT_TEST_USER_USERNAME = "admin"
DEFAULT_TEST_USER_PASSWORD = "admin123"
DEFAULT_TEST_USER_EMAIL = "admin@example.com"
DEFAULT_TEST_USER_ID = 999999


class HardcodedTestUser:
    def __init__(self):
        self.username = getattr(settings, "TEST_USER_USERNAME", DEFAULT_TEST_USER_USERNAME)
        self.email = getattr(settings, "TEST_USER_EMAIL", DEFAULT_TEST_USER_EMAIL)
        self.id = getattr(settings, "TEST_USER_ID", DEFAULT_TEST_USER_ID)
        self.pk = self.id
        self.is_active = True
        self.is_staff = True
        self.is_superuser = True
        self.backend = "loteria.auth_backends.HardcodedTestUserBackend"
        self._meta = get_user_model()._meta
        self.last_login = None

    def save(self, *args, **kwargs):
        # No-op save to avoid database writes for the hardcoded test user.
        return self

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_username(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_session_auth_hash(self):
        return "hardcoded-test-user"

    def __str__(self):
        return self.username


class HardcodedTestUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        valid_username = getattr(settings, "TEST_USER_USERNAME", DEFAULT_TEST_USER_USERNAME)
        valid_password = getattr(settings, "TEST_USER_PASSWORD", DEFAULT_TEST_USER_PASSWORD)
        if username == valid_username and password == valid_password:
            return HardcodedTestUser()
        return None

    def get_user(self, user_id):
        valid_id = getattr(settings, "TEST_USER_ID", DEFAULT_TEST_USER_ID)
        if str(user_id) == str(valid_id):
            return HardcodedTestUser()
        return None
