from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import *

app_name = 'main'

urlpatterns = [
    url(r'^$', MainPage.as_view(), name='main_page'),
    url(r'^registration/(?P<pk>\d+)/$', RegisterUser.as_view(), name='registration'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^(?P<subscription_id>\d+)/(?P<user_id>\d+)/$', InSubscription.as_view(), name='insubs'),
    url(r'^(?P<subscription_id>\d+)/$', UnSubscription.as_view(), name='unsubs'),
    url(r'^send-happy/$', LayoutBD.as_view(), name='layout_bd'),
    url(r'^open-email/(?P<pk>\d+)/$', CheckEmail.as_view(), name="email_view"),
    url(r'^send-news/$', SendNews.as_view(), name='send_news'),
    url('^tasks/$', RenderTasks.as_view(), name='tasks'),
]