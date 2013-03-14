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
import urlparse

from django.contrib import auth
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView
from django.utils.translation import ugettext_lazy as _
from sky_visitor.backends import auto_login
from sky_visitor.forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    model = auth.get_user_model()
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


# Originally from: https://github.com/stefanfoulis/django-class-based-auth-views/blob/develop/class_based_auth_views/views.py
class LoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.

    Usage:
        in urls.py:
            url(r'^login/$',
                LoginView.as_view(
                    form_class=MyVisitorFormClass,
                    success_url='/my/custom/success/url/),
                name="login"),

    """
    redirect_field_name = auth.REDIRECT_FIELD_NAME
    success_url_overrides_redirect_field = False
    template_name = 'sky_visitor/login.html'
    form_class = LoginForm

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log them in.
        """
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        This will default to the "next" field if available, unless success_url_overrides_redirect_field is True, then it will default to that.
        """
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

        # Ensure the user-originating redirection url is safe.
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        if self.success_url and (self.success_url_overrides_redirect_field or not redirect_to):
            redirect_to = self.success_url

        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)
