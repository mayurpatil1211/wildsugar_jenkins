from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth import get_user_model

#-----App Sytem Import
from master_app.models import *
from master_app.serializers import *
#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize

from auth_app.models import *
from auth_app.serializers import *

#----- Decorators
from auth_app.decorators.check_permission_decorator import authorize
from django.utils.decorators import method_decorator

import logging

logger = logging.getLogger('debug_file')

User = get_user_model()

from rest_framework_simplejwt.tokens import RefreshToken
# refresh = RefreshToken.for_user(user)

# token = str(refresh.access_token)
# refresh = str(refresh)


class UserLoginApiView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        if request.data:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            if (username or email) and password:
                if email:
                    user = User.objects.filter(email=email).last()
                elif username:
                    user = User.objects.filter(username=username).last()
                
                if user:
                    password_status = user.check_password(password)
                    if password_status:
                        refresh = RefreshToken.for_user(user)
                        token = str(refresh.access_token)
                        refresh = str(refresh)
                        serializer = UserSerializer(user)
                        return JsonResponse({'message':'User credentials are valid.', 'status':True, 'status_code':200, 'user':serializer.data, 'token':token}, status=200)
                    return JsonResponse({'message':'Invalid Password.', 'status':False, 'status_code':400}, status=400)
                return JsonResponse({'message':'Invalid Username / Email.', 'status':False, 'status_code':400}, status=400)
            return JsonResponse({'message':'Username/Email ID and Password Required.', 'status':False, 'status_code':200}, status=400)
        return JsonResponse({'message':'Bad Request.', 'status':False, 'status_code':400}, status=400)
                    

# from django.utils.decorators import method_decorator

class TestAuth(APIView):
    # @authenticate
    # @method_decorator(authorize('create_user'))
    @authorize('create_user')
    def get(self, request):
        return JsonResponse({'message':'Success'})