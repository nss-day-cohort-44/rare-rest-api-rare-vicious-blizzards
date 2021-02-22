import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rareapi.models import RareUser

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a rare user

    Method arguments: 
        request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    #if the request is an HTTP POST,  try to pull out the relevant info
    if request.method == 'POST':

        #Use the build-in auth method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If auth was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new rare user for auth

    Method arguments:
        request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create new user by invoking the `create_user` helper method
    # on Django's build-in User model
    new_user = User.objects.create_user
    