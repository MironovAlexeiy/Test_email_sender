from __future__ import unicode_literals

import os

from send_message import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from .models import Subscription, User, MailTrack
from .forms import UserCreationForm, SignUser
from .utils import MyMixin
from .tasks import send_registration_mail,send_subscribed_mail, send_unsubscribed_mail, send_hb_email, send_subs_email



class MainPage(ListView):
    """
    Display main page
    """

    model = Subscription
    template_name = 'main.html'
    context_object_name = 'subscriptions'


class RegisterUser(View):
    """
    Display the registration form
    """

    template_name = 'registration.html'

    def get(self, request, pk):
        return render(request, self.template_name, {'form': UserCreationForm()})

    def post(self, request, pk):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            subs = Subscription.objects.get(id=pk)
            user.subscriptions.add(subs)
            email = form.cleaned_data.get('email')
            try:
                send_registration_mail.delay(email, subs.title)
            except Exception as ex:
                HttpResponse(ex)
            return redirect('main:login')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class UserLogin(View):
    """
    Display the login form
    """

    template_name = 'login.html'
    def get(self, request):
        form = SignUser()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = SignUser(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})

class InSubscription(View):
    """
    Subscription on news and send mail user
    """

    def post(self, request, subscription_id, user_id ):
        subscription = Subscription.objects.get(id=subscription_id)
        user = User.objects.get(id=user_id)
        user.subscriptions.add(subscription)
        user.save()
        send_subscribed_mail.delay(user.email, user.get_full_name(), subscription.title)
        return redirect('/')

class UnSubscription(View):
    """
    Unsubscription and send mail
    """

    def post(self, request, subscription_id):
        user = request.user
        subscription = Subscription.objects.get(id=subscription_id)
        user.subscriptions.remove(subscription)
        user.save()
        send_unsubscribed_mail.delay(user.email, user.get_full_name(), subscription.title)
        return redirect('/')


class LayoutBD(MyMixin, View):
    """
    Congratulations to users who have a birthday today.
    Template #1
    """
    def get(self, request):
        template = 'layouts/layout_BD.html'
        subject = 'birthday discount'
        for pk, full_name, birth_day, email in self.get_user_birth_info():
            context = {
                'full_name': full_name,
                'birth_day': birth_day,
                'image_url': settings.PROJECT_DOMAIN + '/open-email/?pk={}'.format(pk)
                }
            try:
                send_hb_email.delay(template, subject, email, context)
                new_track = MailTrack(email=email)
                new_track.save()
            except:
                return HttpResponse('Letters not sent to {}'.format(email))
        return HttpResponse('Letters sent')

class SendNews(MyMixin, View):
    """
    Send an email to the selected category
    """
    def post(self, request):
        template = 'layouts/subscription_layout.html'
        subject = 'News'
        cat_id = request.POST.get('section')
        for id, full_name, email in self.get_emails():
            section = Subscription.objects.get(pk=cat_id).title
            context = {
                'section': section,
                'full_name': full_name,
                'image_url': settings.PROJECT_DOMAIN + '/open-email/?pk={}'.format(id)
            }
            try:
                send_subs_email.delay(template, subject, email, context)
                # send_subs_email.apply_async((template, subject, email, context), countdown=60)
                new_track = MailTrack(email=email)
                new_track.save()
            except:
               return HttpResponse('email not send to {}'.format(email))
        return HttpResponse('All emails been sent')


class CheckEmail(View):
    """
    Checking the opening of the letter
    """
    def get(self, request, pk):
        email = User.objects.get(pk=pk).email
        check_status = MailTrack.objecst.get(email=email)
        check_status.view = True
        check_status.save()
        image = open(os.path.join('main', 'static/img/1x1.png'), 'rb').read()
        return HttpResponse(image, content_type='image/png')


class RenderTasks(View):
    """
    Dispaly task for staff
    """
    def get(self, request):
        return render(request, 'layouts/tasks.html')