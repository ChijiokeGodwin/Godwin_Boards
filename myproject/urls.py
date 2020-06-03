"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, reverse_lazy

from accounts import views as accounts_views
from boards import views

urlpatterns = [
     path('', views.BoardListView.as_view(), name='home'),
     path('signup/', accounts_views.signup, name='signup'),
     path('login/', auth_views.LoginView.as_view(template_name='boards/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),

     path('reset/',
         auth_views.PasswordResetView.as_view(
             template_name='boards/password_reset.html',
             email_template_name='boards/password_reset_email.html',
             subject_template_name='boards/password_reset_subject.txt' ),
         name='password_reset'),
     path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(
              template_name='boards/password_reset_done.html'
            ),
         name='password_reset_done'),
     re_path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         auth_views.PasswordResetConfirmView.as_view(template_name='boards/password_reset_confirm.html'),
         name='password_reset_confirm'),
     path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='boards/password_reset_complete.html'),
         name='password_reset_complete'),

     path('settings/account/',
         accounts_views.UserUpdateView.as_view(), name='my_account'),
     path('settings/password/',
         auth_views.PasswordChangeView.as_view(template_name='boards/password_change.html'),
         name='password_change'),
     path('settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='boards/password_change_done.html'),
         name='password_change_done'),
     
     path('board/new/', views.new_board, name='new_board'),
     re_path('boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/',
          views.reply_topic, name='reply_topic'),
     re_path('boards/(?P<pk>\d+)/new/', views.new_topic, name='new_topic'),
     re_path('boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/',
          views.PostUpdateView.as_view(), name='edit_post'),
     re_path('boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/delete/',
          views.PostDeleteView.as_view(), name='delete_post'),
     re_path('boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/',
          views.PostListView.as_view(), name='topic_posts'),
     re_path('boards/(?P<pk>\d+)/', views.TopicListView.as_view(), name='board_topics'),
     
     
     
     path('admin/', admin.site.urls),
    
    
    
    

    


]
