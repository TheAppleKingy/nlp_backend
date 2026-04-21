import jwt
import time

from typing import Optional

from nlp.application.interfaces.services import AuthServiceInterface


class JWTAuthService(AuthServiceInterface):
    def __init__(self, secret: str, exp: int):
        self._secret = secret
        self._exp = exp

    def get_user_id(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=["HS256"],
                options={"require": ["exp"], "verify_exp": True}
            )
            return payload.get("user_id")
        except:
            return None

    def generate_user_token(self, user_id: int) -> str:
        return jwt.encode(
            {"user_id": user_id, "exp": time.time() + self._exp},
            self._secret,
            algorithm="HS256"
        )
