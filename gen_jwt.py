import jwt
import datetime

def generate_jwt(consumerId, iss, aud, scope, kid, algo, privateKey):
    """Generates the JSON Web Token.

        Args:
            consumerId (str): User.
            iss (str): Issuer of the JWT.
            aud (str): Recipient for which the JWT is intended.
            scope (str): Necessary permissions (scope of access).
            kid (str): The unique identifier for the key.
            algo (str): The specific cryptographic algorithm used with the key (ES256, ES384, ES512, RS256, RS384, etc.).
            privateKey (str): PEM formatted private key.

        Returns:
            str: JSON Web Token.
    """

    payload = {
            "sub": consumerId,
            "iss": iss,
            "aud": aud,
            "exp": int((datetime.datetime.now() + datetime.timedelta(weeks=+4)).timestamp()),
            "iat": int(datetime.datetime.now().timestamp()),
            "scope": scope
    }

    headers = {
        "kid": kid,
    }
    
    return jwt.encode(payload, privateKey, algorithm=algo, headers=headers)

def validateJwt(publicKey, authToken, aud, alg):
    """Validates the JWT.

        Args:
            authToken (str): JWT auth token.
            publicKey (str): Public key used for validation.
            aud (str): Recipient for which the JWT is intended.
            algo (str): The specific cryptographic algorithm used with the key (ES256, ES384, ES512, RS256, RS384, etc.).

        Returns:
            bool: True if validation is succesfull else False.
    """
        
    try:
        jwt.decode(authToken, publicKey, algorithms=[alg], audience=aud)
        return True
    except jwt.exceptions.InvalidSignatureError:
        return False

if __name__ == '__main__':
    pass
    # testing
    # token = generate_jwt("consumerId", ISS, AUD, SCOPE, KID, ALGO, PRIVATE_KEY)
    # print(token)
    # decoded = validateJwt(PUBLIC_KEY, token, ALGO)
    # print(decoded)