from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def create_token(identity):
    return create_access_token(identity=identity)

# Export jwt_required for use in routes
jwt_required = jwt_required
