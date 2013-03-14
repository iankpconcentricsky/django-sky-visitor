# Copyright 2012 Concentric Sky, Inc.
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

from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _
from sky_visitor.backends import auto_login
from sky_visitor.forms import RegisterForm


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'sky_visitor/register.html'
    success_message = _("Successfully registered and logged in")
    login_on_success = True

    def get_form_class(self):
        return RegisterForm

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        user = self.object
        if self.login_on_success:
            auto_login(self.request, user)
        messages.success(self.request, self.success_message)
        return response

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL
