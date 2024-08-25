from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username,**extra_fields):
        """
        Creates and saves a User with the given username.
        """
        if not username:
            raise ValueError('The given username must be set')
        # username = self.normalize_email(username)
        user = self.model(username=username,**extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, **extra_fields)

    def create_superuser(self, username, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        print(username, '------------')
        return self._create_user(username, **extra_fields)