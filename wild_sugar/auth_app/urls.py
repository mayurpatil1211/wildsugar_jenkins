from django.urls import include, path, re_path

from auth_app.apis import login_api
from auth_app.apis.user_management import roles, permissions, list_user

urlpatterns = [
    re_path(r'^user/list/dummy$', list_user.ListUserDummy.as_view(), name='list_user'),
	re_path(r'^login$', login_api.UserLoginApiView.as_view(), name='user_login'),
    re_path(r'^test', login_api.TestAuth.as_view(), name='api'),
    
    #-------Roles
    re_path(r'^roles$', roles.RolesAPIView.as_view(), name='roles'),
    re_path(r'^roles/permission$', roles.AttachPermissionApiView.as_view(), name='role_permission'),
    re_path(r'^roles/users$', roles.AttachRolesUser.as_view(), name='roles_user'),
    
    #------- Permissions
    re_path(r'^permissions$', permissions.PermissionApiView.as_view(), name='permissions'),
	
]
