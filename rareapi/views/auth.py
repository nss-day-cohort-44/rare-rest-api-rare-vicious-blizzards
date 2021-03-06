import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rareapi.models import RareUser
import datetime

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
        username = req_body['email']
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
    new_user = User.objects.create_user(
        username = req_body['username'],
        email = req_body['email'],
        password = req_body['password'],
        first_name = req_body['firstName'],
        last_name = req_body['lastName']
    )

    # Now save the extra info in the rareapi_rare_user table

    rare_user = RareUser.objects.create(
        created_on = datetime.datetime.today(),
        user = new_user,
        active = True
    )

    # Commit the user to the database by saving it
    rare_user.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    #Return the token to the client
    data = json.dumps({"token": token.key, "valid": True})
    return HttpResponse(data, content_type='application/json')