from rest_framework import serializers

from master_app.models import *
from auth_app.models import *

from django.conf import settings

from django.contrib.auth import get_user_model




User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

#-----Permission
class PermissionSerializer(serializers.ModelSerializer):
    permission_code = serializers.CharField(read_only=True)
    class Meta:
        model = Permissions
        fields = '__all__'  
        
class PermissionBriefSerializer(serializers.ModelSerializer):
    permission_code = serializers.CharField(read_only=True)
    class Meta:
        model = Permissions
        fields = ['permission_code', 'permission_description', 'parent_permission', 'id']     
        
        
#-------ROLES
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
        
class RoleBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['role_name','role_code','in_action', 'id']
        


#-------RolePermission
class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'


class PermissionFromRoleSerializer(serializers.ModelSerializer):
    permission = PermissionBriefSerializer(many=False)
    class Meta:
        model = RolePermission
        fields = ['permission']


class RoleFromPermissionSerializer(serializers.ModelSerializer):
    role = RoleBriefSerializer(many=False)
    class Meta:
        model = RolePermission
        fields = ['role']
    
#-----User roles
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'
        
        