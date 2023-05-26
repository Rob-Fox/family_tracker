from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re, bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')


class EventManager(models.Manager):
    def validator(self, postData):
        errors = {}
        return errors

class Event(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name='creator',
        null=True
    )


    objects = EventManager()

    def __repr__(self):
        return {
            'name': {},
            'creator': {}
        }

class Group(models.Model):
    name = models.CharField(max_length=254)
    members = models.ManyToManyField('User', blank=False)
    events = models.ManyToManyField('Event', blank=True)

    def __repr__(self):
        return {
            'Name': self.name,
            'Members': self.members,
            'Events': self.events
        }

class Calendar(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user')


    def __repr__(self):
        return {
            'User': self.user
        }

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = 'Name must be at least 3 characters.'
        if not NAME_REGEX.match(postData['name']):
            errors['name'] = 'Name must be comprised of letters only.'
        if len(postData['username']) < 5:
            errors['username'] = 'Username must be at least 5 characters.'
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors['email'] = 'Please enter a valid email address.'
        if User.objects.filter(email=postData['email']):
            errors['email'] = 'There is already an account tied to that email.'
        if User.objects.filter(username=postData['username']):
            errors['username'] = 'That username is already taken, please try another.'
        if len(postData['password']) < 8:
            errors['password'] = 'Please create a password that is 8 characters or longer.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match, please check them and try again.'
        return errors

    def login_validator(self, postData):
        errors = {}
        if not User.objects.get(username=postData['username']):
            errors['login'] = 'Username or password is incorrect.'
        if User.objects.get(username=postData['username']):
            if not bcrypt.checkpw(postData['login_password'].encode(), User.objects.get(username=postData['username']).password.encode()):
                errors['login'] = 'Username or password is incorrect.'
        return errors

class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=254)
    token = models.BinaryField(unique=True)
    groups = models.ManyToManyField(
        'Event',
        blank=True)
    calendar = models.ForeignKey(
        'Calendar',
        on_delete=models.SET_NULL,
        related_name='calendar',
        null=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['token'])
        ]

    def __repr__(self):
        return {
            'Name': {self.name},
            'Username': {self.username},
            'Password': {self.password}
        }

    # def to_dict(self):
    #     return {
    #         'name': self.name,
    #         'email': self.email,
    #         'username': self.,
    #         'password': ,
    #         'groups': ,
    #         'calendar': self.calendar
    #     }

