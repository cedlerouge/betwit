from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager

class User(AbstractBaseUser, PermissionsMixin):
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
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = u'user'

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        fullname = self.first_name+" "+self.last_name
        return self.fullname

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

