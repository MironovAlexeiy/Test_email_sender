from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Subscription, MailTrack

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Displaying the model User in the admin panel
    """
    fields = ('first_name', 'last_name', 'email', 'birth_day', 'subscriptions', 'username', 'is_active', 'password')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Displaying the model Subscription in the admin panel
    """
    fields = ('title', 'image',)

@admin.register(MailTrack)
class MailTrackAdmin(admin.ModelAdmin):
    """
    Displaying the model MailTrack in the admin panel
    """
    fields = ('email', 'view', )
    list_display = ('email', 'view', )