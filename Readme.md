# JWT Web service

Web service to return [JSON Web Token (JWT)](https://auth0.com/docs/secure/tokens/json-web-tokens) for authentication.

# Configure web service

A configuration file needs to be passed to the JWT web service on start.

**`jwt.properties`**
```bash

PRIVATE_KEY=""
PUBLIC_KEY=""
ISS=""
AUD=""
SCOPE=""
KID=""
ALGO=""
USERNAME=""
PASSWORD_HASH=""
```

**PRIVATE_KEY** - Private key to sign the JWT.

**PUBLIC_KEY** - Public key to verify the JWT.

`openssl` can be used to generate the private key.

```bash
>> openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem
>> openssl pkcs8 -in private-key.pem -topk8 -nocrypt -out key.pk8
>> cat key.pk8
-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgAKuj+/OE4vm5XB28
/+zMSsUAdudgqHY5g2moR+5wpj2hRANCAAR3aoFEIaT2I91j4ZtpkPWWJDxeKPaE
YqzkGj3GP4YpWQFQG+DxWBEFQuhlPJnvqs1R4Eg4mngs/pHpZ+0XgRwR
-----END PRIVATE KEY-----
>> openssl ec -in private-key.pem -pubout > public.pem
>>cat public.pem
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEd2qBRCGk9iPdY+GbaZD1liQ8Xij2
hGKs5Bo9xj+GKVkBUBvg8VgRBULoZTyZ76rNUeBIOJp4LP6R6WftF4EcEQ==
-----END PUBLIC KEY-----
```

**ALGO** - The specific cryptographic algorithm used with the key (`ES256`, `ES384`, `ES512`, `RS256`, `RS384`, etc.).

**ISS** - Issuer of the JWT.

**AUD** - Recipient for which the JWT is intended.

**SCOPE** - Necessary permissions (scope of access).

**KID** - The unique identifier for the key.

**USERNAME** - Username for API authentication, can have any value

**PASSWORD_HASH** - SHA256 password hash of the password used for API authentication. The hash can be obtained using some hasing tool.

```bash
>> echo -n "my_secret_password" | shasum -a 256
6586bc035202dff98a67b814aca615e613cbbfae8ffa8f4a475da0faef079c9d
```

Example `jwt.properties` file.

**`jwt.properties`**
```bash

PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgAKuj+/OE4vm5XB28/+zMSsUAdudgqHY5g2moR+5wpj2hRANCAAR3aoFEIaT2I91j4ZtpkPWWJDxeKPaEYqzkGj3GP4YpWQFQG+DxWBEFQuhlPJnvqs1R4Eg4mngs/pHpZ+0XgRwR\n-----END PRIVATE KEY-----"
PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEd2qBRCGk9iPdY+GbaZD1liQ8Xij2hGKs5Bo9xj+GKVkBUBvg8VgRBULoZTyZ76rNUeBIOJp4LP6R6WftF4EcEQ==\n-----END PUBLIC KEY-----"
ISS="https://example.io/oidc/d1_sandbox"
AUD="https://example.io/oidc/d1_sandbox"
SCOPE="user:write"
KID="kid_1"
ALGO="ES256"
USERNAME="my_user"
PASSWORD_HASH="6586bc035202dff98a67b814aca615e613cbbfae8ffa8f4a475da0faef079c9d"
```

# Running the web service

## Docker

The service is composed as a [docker](https://www.docker.com) image.

```bash
# build docker image
>> docker build --no-cache . -t user/tag
# run docker image
>> docker run -d -p 3002:80 -v /path/to/jwt.properties:/etc/config/jwt.properties user/tag
```

# Access and test web service

[curl](https://curl.se) examples of accessing the web service API.

```bash
# LEGACY API
>> curl -u "my_user:my_secret_password" http://127.0.0.1:3002/protected/sandbox/jwt/<consumer_id>
>> curl -u "my_user:my_secret_password" -X POST http://127.0.0.1:3002/protected/sandbox/jwt/ -H "Content-Type: application/json" -d '{"consumer_id" : "<consumer_id>"}'
>> curl -u "my_user:my_secret_password" -X POST http://127.0.0.1:3002/protected/sandbox/validate/ -H "Content-Type: application/json" -d '{"jwt" : "<jwt>"}'
```

```bash
>> curl -u "my_user:my_secret_password" http://127.0.0.1:3002/v2/protected/sandbox/jwt/<consumer_id>
>> curl -u "my_user:my_secret_password" -X POST http://127.0.0.1:3002/v2/protected/sandbox/jwt/ -H "Content-Type: application/json" -d '{"consumer_id" : "<consumer_id>"}'
>> curl -u "my_user:my_secret_password" -X POST http://127.0.0.1:3002/v2/protected/sandbox/validate/ -H "Content-Type: application/json" -d '{"jwt" : "<jwt>"}'
```

# References

[JSON Web Token (JWT)](https://auth0.com/docs/secure/tokens/json-web-tokens).

[curl](https://curl.se).

[docker](https://www.docker.com).
