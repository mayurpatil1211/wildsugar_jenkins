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


class RolesAPIView(APIView):
    permission_classes = (AllowAny,)
    @authorize('register_role')
    def post(self, request):
        if request.data:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'Role Registered Successfully.', 'status':True, 'status_code':201, 'result':serializer.data}, status=201)
            return JsonResponse({'message':'Error during registering role.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
        return JsonResponse({'message':'Bad request.', 'status':False, 'status_code':400}, status=400)
    
    @authorize('update_role')
    def put(self, request):
        _id = request.data.get('id')
        if _id:
            role = Roles.objects.filter(id=_id).last()
            if role:
                serializer = RoleSerializer(role, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'Role updated successfully.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
                return JsonResponse({'message':'Error during updating role information.', 'status':False, 'status_code':400, 'error':serializer.errors}, status=400)
            return JsonResponse({'message':'Invalid role id.', 'status':False, 'status_code':400}, status=400)
        return JsonResponse({'message':'Role ID required.', 'status':False, 'status_code':400}, status=400)

    
    def get(self, request):
        _id = request.GET.get('id')
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        end = int(page)*int(count_per_page)
        start = end - int(count_per_page)
        
        if _id:
            role = Roles.objects.filter(id=_id).last()
            serializer = RoleSerializer(role)
            return JsonResponse({'message':'Role Details.', 'status':True, 'status_code':200, 'result':serializer.data}, status=200)
        roles = Roles.objects.all()[start:end]
        serializer = RoleSerializer(roles, many=True)
        count = Roles.objects.count()
        return JsonResponse({'message':'Roles list.', 'status':False, 'status_code':200, 'result':serializer.data, 'count':count}, status=200)
    
    @authorize('delete_role')
    def delete(self, request):
        _id = request.GET.get('id')
        Roles.objects.filter(id=_id).update(in_action=False)
        return JsonResponse({'message':'Role Deleted Successfully.', 'status':True, 'status_code':200}, status=200)



class AttachPermissionApiView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        role = request.GET.get('role', None)
        permission = request.GET.get('permission', None)
        page = request.GET.get('page', 1)
        count_per_page = request.GET.get('count_per_page', 20)
        
        end = int(page)*int(count_per_page)
        start = end-int(count_per_page)
        if role:
            role_instance = RolePermission.objects.filter(role=role).all()[start:end]
            serializer = PermissionFromRoleSerializer(role_instance, many=True)
            count = RolePermission.objects.filter(role=role).count()
            return JsonResponse({'message':'Permission of requested Role.', 'status':True, 'status_code':200, 'permissions':serializer.data, 'count':count}, status=200)
        elif permission:
            role_instance = RolePermission.objects.filter(permission=permission).all()[start:end]
            serializer = RoleFromPermissionSerializer(role_instance, many=True)
            count = RolePermission.objects.filter(permission=permission).count()
            return JsonResponse({'message':'Roles of requested Permission.', 'status':True, 'status_code':200, 'permissions':serializer.data, 'count':count}, status=200)
        else:
            return JsonResponse({'message':'Invalid Request.', 'status':False, 'status_code':400}, status=400)
        
    @authorize('attach_permission')
    def post(self, request):
        roles = request.data.get('roles', [])
        permissions = request.data.get('permission', [])
        errors = []
        if roles and permissions:
            for role in roles:
                errors.extend(self.map_permission(role, permissions))
        return JsonResponse({'message':'Permission Attached to role successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)

    
    def map_permission(self, role_id, permissions):
        error = []
        for permission in permissions:
            serializer = RolePermissionSerializer(data={
                'role':role_id,
                'permission':permission
            })
            
            if serializer.is_valid():
                serializer.save()
            else:
                error.append(serializer.errors)
        return error
    
    
    @authorize('dettach_permission')
    def delete(self, request):
        roles = request.data.get('roles', [])
        permissions = request.data.get('permission', [])
        errors = []
        if roles and permissions:
            for role in roles:
                errors.extend(self.demap_permission(role, permissions))
        return JsonResponse({'message':'Permission removed from role successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)
    
    def demap_permission(self,role_id, permissions):
        RolePermission.objects.filter(role=role_id).filter(permission__in=permissions).delete()
        return True
    
    
class AttachRolesUser(APIView):
    permission_classes = (AllowAny,)
    @authorize('attach_roles')
    def post(self, request):
        users = request.data.get('users', [])
        roles = request.data.get('roles', [])
        errors = []
        if roles and users:
            for user in users:
                errors.extend(self.map_roles(user, roles))
        return JsonResponse({'message':'Roles Attached to User successfully.', 'status':True, 'status_code':200, 'error':errors}, status=200)

    
    def map_roles(self, user_id, roles):
        error = []
        for role in roles:
            serializer = UserRoleSerializer(data={
                'user':user_id,
                'role':role
            })
            
            if serializer.is_valid():
                serializer.save()
            else:
                error.append(serializer.errors)
        return error
    
    @authorize('dettach_roles')
    def delete(self, request):
        users = request.data.get('users', [])
        roles = request.data.get('roles', [])
        
        if users and roles:
            for user in users:
                self.dettach_role(user, roles)
            return JsonResponse({'message':'Role removed from user successfully.', 'status':True, 'statu_code':200}, status=200)
        return JsonResponse({'message':'Users and Role IDs required.', 'status':False, 'status_code':400}, status=400)
    
    def dettach_role(self, user_id, roles):
        UserRoles.objects.filter(user=user_id, role__in=roles).delete()
        return True
        