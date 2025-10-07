import unittest

from core.security import decode_jwt, sign_jwt


class MyTest(unittest.TestCase):
    def test_jwt_code_decode(self):
        user_id = 1
        token = sign_jwt(user_id)
        dico = decode_jwt(token)
        assert dico["sub"], "1"
