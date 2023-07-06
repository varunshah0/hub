from django.contrib.auth import authenticate, get_user_model, login, logout
from firebase_admin import auth
from ninja import ModelSchema, NinjaAPI, Schema
from ninja.security import django_auth

User = get_user_model()

api = NinjaAPI(auth=django_auth, csrf=True)


class Credentials(Schema):
    username: str
    password: str


class FirebaseCredentials(Schema):
    token: str
    uid: str


class Response(Schema):
    message: str


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["username"]


@api.get("/user")
def current_user(request, response={200: UserSchema}):
    return UserSchema.from_orm(request.user)


@api.post("/login", auth=None, response={200: UserSchema, 403: Response})
def api_login(request, credentials: Credentials):
    user = authenticate(request, username=credentials.username, password=credentials.password)
    if user is not None:
        login(request, user)
        return 200, UserSchema.from_orm(user)
    else:
        return 403, {"message": "Invalid credentials"}


@api.post("/logout")
def api_login(request):
    logout(request)


@api.post("/firebase-login", auth=None, response={200: UserSchema, 403: Response})
def login(request, credentials: FirebaseCredentials):
    firebase_user = auth.get_user(credentials.uid)
    invalid_credentials = 403, {"message": "Invalid credentials"}
    if firebase_user is None:
        return invalid_credentials

    try:
        # FIXME: Handle login using email
        # FIXME: Decide on how to handle new sign-ups
        user = User.objects.get(phone=firebase_user.phone_number)
    except User.DoesNotExist:
        return invalid_credentials

    request.session["firebase_token"] = credentials.token
    request.user = user
    return 200, UserSchema.from_orm(user)
