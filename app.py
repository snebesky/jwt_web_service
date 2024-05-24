from flask import Flask, request, jsonify
from gen_jwt import generate_jwt, validateJwt
import hashlib
from flask_httpauth import HTTPBasicAuth

"""JWT Web Service entry point.

Usage:
>> curl -u "username:password" -X GET http://url/protected/sandbox/jwt/<consumer_id>
>> curl -u "username:password" -X POST http://url/protected/sandbox/jwt/ -H "Content-Type: application/json" -d '{"consumer_id" : "<consumer_id>"}'
>> curl -u "username:password" -X POST http://url/protected/sandbox/validate/ -H "Content-Type: application/json" -d '{"jwt" : "<jwt>"}'
"""

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config.from_pyfile("/etc/config/jwt.properties", silent=False)

iss = app.config.get("ISS")
aud = app.config.get("AUD")
scope = app.config.get("SCOPE")
kid = app.config.get("KID")
algo = app.config.get("ALGO")
username = app.config.get("USERNAME")
password_hash = app.config.get("PASSWORD_HASH")
privateKey = app.config.get("PRIVATE_KEY")
publicKey = app.config.get("PUBLIC_KEY")

users = {
    username: password_hash,
}

@app.route("/protected/sandbox/jwt/<string:consumerId>", methods=["GET"])
@auth.login_required
def getJwtProtectedGet(consumerId):
    return generate_jwt(consumerId, iss, aud, scope, kid, algo, privateKey)

@app.route("/v2/protected/sandbox/jwt/<string:consumerId>", methods=["GET"])
@auth.login_required
def getJwtProtectedGetV2(consumerId):
    jwt = generate_jwt(consumerId, iss, aud, scope, kid, algo, privateKey)
    return jsonify({"access_token" : jwt} )

@app.route("/protected/sandbox/jwt/", methods=["POST"])
@auth.login_required
def getJwtProtectedPost():
    data = request.json
    consumerId = data.get('consumer_id')
    if consumerId is None:
        return "Missing mandatory parameter in request: consumer_id", 400
    
    return generate_jwt(consumerId, iss, aud, scope, kid, algo, privateKey)

@app.route("/v2/protected/sandbox/jwt/", methods=["POST"])
@auth.login_required
def getJwtProtectedPostV2():
    data = request.json
    consumerId = data.get('consumer_id')
    if consumerId is None:
        return "Missing mandatory parameter in request: consumer_id", 400
    
    jwt = generate_jwt(consumerId, iss, aud, scope, kid, algo, privateKey)
    return jsonify({"access_token" : jwt} )

@app.route("/protected/sandbox/validate/", methods=["POST"])
@auth.login_required
def validateJwtPost():
    data = request.json
    jwt = data.get('jwt')
    if jwt is None:
        return "Missing mandatory parameter in request: jwt", 400
    
    if validateJwt(publicKey, jwt, aud, algo):
        return "SIGNATURE_VERIFICATION_OK"
    else:
        return "SIGNATURE_VERIFICATION_FAILED"
    
@app.route("/v2/protected/sandbox/validate/", methods=["POST"])
@auth.login_required
def validateJwtPostV2():
    data = request.json
    jwt = data.get('jwt')
    if jwt is None:
        return "Missing mandatory parameter in request: jwt", 400
    
    if validateJwt(publicKey, jwt, aud, algo):
        return jsonify({"status" : "SIGNATURE_VERIFICATION_OK"})
    else:
        return jsonify({"status" : "SIGNATURE_VERIFICATION_FAILED"})

@auth.verify_password
def authenticate(username, password):
    if username and password:
        hash = hashlib.sha256()
        hash.update(password.encode('utf-8'))
        hashedPassword = hash.hexdigest()

        if users.get(username) is not None:
            if users[username] == hashedPassword:
                return True

    return False

if __name__ == '__main__':
    # use for debug
    # app.run(host='0.0.0.0', port=80)
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
