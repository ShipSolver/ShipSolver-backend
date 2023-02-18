from flask import session

class IdentityHelper:

    @staticmethod
    def get_logged_in_userId():
        claims = session.get("claims")
        if claims and "sub" in claims:
            return claims["sub"]
        return None