# Copyright 2013 Concentric Sky, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.conf.urls import *
from sky_visitor.views import *

TOKEN_REGEX = '(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^forgot_password/$', ForgotPasswordView.as_view(), name='forgot_password'),
    url(r'^forgot_password/check_email/$', ForgotPasswordCheckEmailView.as_view(), name='forgot_password_check_email'),
    url(r'^reset_password/%s/$' % TOKEN_REGEX, ResetPasswordView.as_view(), name='reset_password'),
    url(r'^change_password/$', ChangePasswordView.as_view(), name='change_password'),
    url(r'invitation/$', InvitationStartView.as_view(), name='invitation_start'),
    url(r'invitation/%s/$' % TOKEN_REGEX, InvitationCompleteView.as_view(), name='invitation_complete'),
#     url(r'invitation/done/$',   InvitationDoneView.as_view(),   name='invitation_done'),
]
