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


class PermissionApiView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        query = request.GET.get('query', None)
        
        end = int(page)*int(count_per_page)
        start = end - int(count_per_page)
        
        if query:
            permissions = Permissions.objects.filter(queue(permission_code__icontains=query) | queue(permission_description__icontains=query))[start:end]
            count = Permissions.objects.filter(queue(permission_code__icontains=query) | queue(permission_description__icontains=query)).count()
        else:
            permissions = Permissions.objects.all()[start:end]
            count = Permissions.objects.count()
        serializer = PermissionSerializer(permissions, many=True)
        return JsonResponse({'message':'Permission List.', 'status':False, 'status_code':200, 'result':serializer.data}, status=200)
    
    @authorize('update_permission')
    def put(self, request):
        if request.data:
            _id = request.data.get('id')
            if _id:
                permission = Permissions.objects.filter(id=_id).last()
                if permission:
                    serializer = PermissionSerializer(permission, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'message':'Permission Updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                    return JsonResponse({'message':'Error during updating permission', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
                return JsonResponse({'message':'Invalid Permission ID.', 'status':False,'status_code':404}, status=404)
            return JsonResponse({'message':'Permission ID required.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('delete_permission')
    def delete(self, request):
        if request.data:
            _id = request.data.get('id')
            if _id:
                permission = Permissions.objects.filter(id=_id).update(in_action=False)
                return JsonResponse({'message':'Permission Marked Inactive.', 'status':False, 'status_code':200}, status=200)
            return JsonResponse({'message':'Invalid request, Permission ID required.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)