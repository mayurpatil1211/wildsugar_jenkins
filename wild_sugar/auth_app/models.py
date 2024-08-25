from distutils.sysconfig import customize_compiler
from statistics import mode
from django.db import models
from django.conf import settings

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model

from auth_app.manager import UserManager

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

import random
import string
import secrets
import datetime

# > User
# 	- username - required (unique)
# 	- name - required
# 	- email - required / not required (doubt) (unique)
# 	- contact_number - not required
# 	- user_type - required
# 	- password - not required
# 	- active - Boolean (True)
# 	- address - not required
# 	- city - not required
# 	- state - not required
# 	- country - not required (India)
# 	- pan - not required
# 	- adhar - not required
#   - last_login - not required
#   - login_count - not required
#   - blocked - False
#   - profile_picture_link - not required
#   - profile_picture_key - not required
#   - record_date - Default

# > employee_details
# 	- user (FK User) - required
# 	- employeee_code - required (need Format of emaployee id)
# 	- employment_type - required
# 	- referred_by (FK User) - not required
# 	- date_of_joining - not required
# 	- working_hours - not required
# 	- skilled_section - not required
# 	- work_shift - not required (json)
# 	- designation - required
# 	- permitted_advance_limit_percentage - not required

# > UserRoles
# 	- roles
# 	- user (FK User)

# > employee_salary_structure
# 	- user (FK User)
# 	- ctc - required
# 	- basic_salary - required
# 	- hra - required
# 	- dearness_allowance - required
# 	- food_allowance - required
# 	- travel_allowance - required
# 	- esi_pf - required
# 	- bonus - required
# 	- other_allowance - required

class User(AbstractUser):
    name = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=False, unique=True)
    contact_number = models.CharField(max_length=13, null=True, blank=True)
    user_type = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True, default='India')
    pan = models.CharField(max_length=20, null=True, blank=True)
    adhar = models.CharField(max_length=30, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=False)
    login_count = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)
    profile_picture_link = models.TextField(null=True, blank=True)
    profile_picture_key = models.CharField(max_length=100, null=True, blank=True)
    record_date = models.CharField(max_length=100, null=True, blank=True)


    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'auth_app'
        db_table = 'user'
        

        indexes = [
            models.Index(fields=['username', 'email', 'active', 'record_date']),
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]



    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def hash_password(self, raw_password):
        hash_password = make_password(raw_password)
        return hash_password

    # def save(self, *args, **kwargs):
    #     self.username = self.email

    #     super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.email)



@receiver(post_save, sender=User)
def create_hashed_password(sender, instance=None, created=False, **kwargs):
	if created:
		if instance.password:
			hash_password = make_password(instance.password)
			user = User.objects.filter(id=instance.id).first()
			user.password = hash_password
			user.recepient_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))+'-'+\
								str(datetime.datetime.now().day)+''+str(datetime.datetime.now().month)+''+str(datetime.datetime.now().year)+''+\
								str(datetime.datetime.now().hour)+''+str(datetime.datetime.now().minute)+''+str(datetime.datetime.now().second)
			user.save()




class Permissions(models.Model):
    permission_description = models.CharField(max_length=240, null=False, blank=False)
    permission_code = models.CharField(max_length=240, null=False, blank=False)
    parent_permission = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    in_action = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'auth_app'
        db_table = 'permissions'
        

        indexes = [
            models.Index(fields=['permission_code', 'parent_permission']),
            models.Index(fields=['permission_code']),
            models.Index(fields=['parent_permission']),
            models.Index(fields=['permission_description']),
        ]
    
    
class Roles(models.Model):
    role_name = models.CharField(max_length=240, null=False, blank=False)
    role_code = models.CharField(max_length=240, null=False, blank=False)
    in_action = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'auth_app'
        db_table = 'roles'
        

        indexes = [
            models.Index(fields=['role_code', 'role_name']),
            models.Index(fields=['role_code']),
            models.Index(fields=['role_name']),
            models.Index(fields=['in_action']),
        ]
        
class RolePermission(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permissions, on_delete=models.CASCADE, related_name='roles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'auth_app'
        db_table = 'role_permissions'
        
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['permission']),
        ]


class UserRoles(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='user_roles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'auth_app'
        db_table = 'user_roles'
        
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['user']),
        ]