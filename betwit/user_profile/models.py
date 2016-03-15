from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager

class User(AbstractBaseUser):
    """
    Custom user class
    """
    username	= models.CharField('username', max_length=15, unique=True, db_index=True)
    first_name	= models.CharField(default='first name', max_length=15)
    last_name	= models.CharField(default='last name', max_length=15)
    email	= models.EmailField('email address', unique=True)
    joined	= models.DateTimeField(auto_now_add=True)
    is_active	= models.BooleanField(default=True)
    is_staff	= models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        db_table = u'user_profile_user'

    def __unicode__(self):
        return self.username


