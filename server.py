import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from models import Session, User, Advertisement
from schema import CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement

app = Flask('app')
bcrypt = Bcrypt(app)


def hash_password(password: str):
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()

def check_password(password: str, hashed_password: str):
   password = password.encode()
   hashed_password = hashed_password.encode()
   return bcrypt.check_password_hash(password, hashed_password)

def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response
def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user

def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "user already exists")
class UserView(MethodView):

    def get(self, user_id):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(CreateUser, request.json)
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id):
        json_data = validate(UpdateUser, request.json)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_user_by_id(user_id)
        for key, value in json_data.items():
            setattr(user, key, value)
        request.session.commit()
        return jsonify(user.dict)

    def delete(self, user_id):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "delete"})

def get_ad_by_id(ad_id: int):
    ad = request.session.query(Advertisement).get(ad_id)
    if ad is None:
        raise HttpError(404, "Advertisement not found")
    return ad

def add_ad(ad: Advertisement):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "ad already exists")

class AdvertisementView(MethodView):
    def get(self, ad_id):
        ad = get_ad_by_id(ad_id)
        return jsonify(ad.dict)

    def post(self):
        json_data = validate(CreateAdvertisement, request.json)
        ad = Advertisement(**json_data)
        add_ad(ad)
        return jsonify(ad.dict)

    def patch(self, ad_id):
        json_data = validate(UpdateAdvertisement, request.json)
        ad = get_ad_by_id(ad_id)
        for key, value in json_data.items():
            setattr(ad, key, value)
        add_ad(ad)
        return jsonify(ad.dict)

    def delete(self, ad_id):
        ad = get_ad_by_id(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"status": "delete"})


user_view = UserView.as_view("user")

app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)


ad_view = AdvertisementView.as_view("ad")

app.add_url_rule("/ad/", view_func=ad_view, methods=["POST"])
app.add_url_rule("/ad/<int:ad_id>", view_func=ad_view, methods=["GET", "PATCH", "DELETE"])

if __name__ == '__main__':
    app.run()



