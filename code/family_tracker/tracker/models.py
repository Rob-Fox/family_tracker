from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re, bcrypt, uuid

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
        return "name: {}, creator: {}".format(self.name, self.creator)

class Group(models.Model):
    name = models.CharField(max_length=254)
    members = models.ManyToManyField('User', blank=False)
    events = models.ManyToManyField('Event', blank=True)

    def __repr__(self):
        return "Name: {}, Members: {}, Events: {}".format(self.name, self.members, self.events)

class Calendar(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user')


    def __repr__(self):
        return "User: {}".format(self.user)

class UserManager(models.Manager):
    def _create_user(self, username, email, password, **xargs):
        """
            creates and saves a user with given email, password, and username
        """
        if not email:
            raise ValueError('Must provide an email')
        if User.objects.filter(email=email):
            raise ValueError('An account is already associated with that email address.')
        try:
            validate_email(email)
        except:
            raise ValueError('Must provide a valid email')
        else:
            email = self.normalize_email(email)
        if not username:
            raise ValueError('Must provide a username')
        if User.objects.filter(username=username):
            raise ValueError('That username is already taken, please try another.')
        user = self.model(email=email, username=username, **xargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **xargs):
        return self._create_user(email, password, **xargs)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        return "Name: {}, Username: {}, Password: {}".format(self.name, self.username, self.password)

    # def to_dict(self):
    #     return {
    #         'name': self.name,
    #         'email': self.email,
    #         'username': self.,
    #         'password': ,
    #         'groups': ,
    #         'calendar': self.calendar
    #     }

