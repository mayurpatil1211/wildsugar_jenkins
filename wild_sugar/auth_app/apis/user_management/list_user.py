from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth import get_user_model

from django.db.models import Q as queue

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


class ListUserDummy(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse({'message':'User list', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)