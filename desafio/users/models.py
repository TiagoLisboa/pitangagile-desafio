from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    firstName = models.EmailField(_('first name'), max_length=30)
    lastName = models.EmailField(_('last name'), max_length=30)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the firstName plus the lastName, with a space in between.
        '''
        full_name = '%s %s' % (self.firstName, self.lastName)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.firstName
