"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
from account import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
app_name = 'account'
urlpatterns = [
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('register/',views.register, name='register'),

    # 密码更改
    re_path(r'password-change/$',
        auth_views.PasswordChangeView.as_view(
            template_name='account/password_change_form.html',
            success_url = reverse_lazy('account:password_change_done'),
        ),
        name='password_change'),
    re_path(r'password-change-done/$',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='account/password_change_done.html'
        ),
        name='password_change_done'),

    # 密码重置邮件发送
    re_path(r'^password-reset/$',
        auth_views.PasswordResetView.as_view(
            template_name = 'account/password_reset_form.html',
            email_template_name = 'account/password_reset_email.html',
            subject_template_name = 'account/password_reset_subject.txt',
            success_url = reverse_lazy('account:password_reset_done'),
        ),
        name='password_reset'),

    # 密码重置邮件发送完成
    re_path(r'^password-reset-done/$',
        # auth_views.password_reset_done,
        auth_views.PasswordResetDoneView.as_view(
            template_name = 'account/password_reset_done.html',
        ),
        name='password_reset_done'),

    # 密码重置确认
    re_path(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',

        auth_views.PasswordResetConfirmView.as_view(
            template_name = 'account/password_reset_confirm.html',
            success_url = reverse_lazy('account:password_reset_complete')
        ),
        name='password_reset_confirm'),

    # 密码重置成功
    re_path(r'^password-reset-complete/$',
        # auth_views.password_reset_complete,
        auth_views.PasswordResetCompleteView.as_view(
            template_name = 'account/password_reset_complete.html',
        ),
        name='password_reset_complete'),
]
