from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
       Model representing a user.
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(unique=True, blank=True)
    birth_day = models.DateField(blank=True, null=True)
    subscriptions = models.ManyToManyField('Subscription', related_name='users')

    def __str__(self):
        """
        String for representing the User object (in Admin site etc.)
        """
        return self.get_full_name()





class Subscription(models.Model):
    """
    Model representing a subscription.
    """
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='img/')


    def __str__(self):
        """
        String for representing the Subscription object (in Admin site etc.)
        """
        return self.title


class MailTrack(models.Model):
    """
    Model for tracking email
    """
    email = models.EmailField(max_length=254)
    view = models.BooleanField(default=False)

    def __str__(self):
        """
        String for representing MailTrack object (in Admin site etc.)
        """
        return self.email