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
from django.utils.text import capfirst
from sky_visitor.forms import LoginForm
from sky_visitor.tests import SkyVisitorTestCase


FIXTURE_USER_DATA = {
    'username': 'testuser',
    'email': 'testuser@example.com',
    'password': 'adminadmin'
}


class SkyVisitorViewsTestCase(SkyVisitorTestCase):

    def setUp(self):
        super(SkyVisitorViewsTestCase, self).setUp()


class RegisterViewTest(SkyVisitorViewsTestCase):
    view_url = '/user/register/'

    def get_test_data(self):
        # Includ
        data = {
            'username': 'registeruser',
            'password1': 'password',
            'password2': 'password',
        }
        return data

    def test_register_view_exists(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        return response

    def test_registration_should_succeed(self):
        UserModel = get_user_model()
        data = self.get_test_data()
        testuser_username = data[UserModel.USERNAME_FIELD]
        response = self.client.post(self.view_url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to '/' (LOGIN_REDIRECT_URL)
        self.assertRedirects(response, '/')
        # Lookup the user based on the username field and the value in the test data
        self.assertEqual(UserModel._default_manager.filter(**{UserModel.USERNAME_FIELD: testuser_username}).count(), 1)

    def test_registration_should_fail_on_mismatched_password(self):
        data = self.get_test_data()
        data['password2'] = 'mismatch'
        response = self.client.post(self.view_url, data=data)
        self.assertEqual(response.status_code, 200)
        form = response.context_data['form']
        # Form should have errors for mismatched password
        self.assertEqual(len(form.errors), 1)
        self.assertIn('password2', form.errors)


class LoginViewTest(SkyVisitorViewsTestCase):
    view_url = '/user/login/'

    def test_login_form_should_exist(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_login_form_should_succeed(self):
        UserModel = get_user_model()
        data = {
            # Always use username as the field name because that's how contrib.auth.forms.AuthenticationForm is built
            'username': FIXTURE_USER_DATA[UserModel.USERNAME_FIELD],
            'password': FIXTURE_USER_DATA['password'],
        }
        response = self.client.post(self.view_url, data)
        # Should redirect
        self.assertRedirected(response, '/')

        # Should be logged in
        user = UserModel._default_manager.get(**{UserModel.USERNAME_FIELD: FIXTURE_USER_DATA[UserModel.USERNAME_FIELD]})
        self.assertLoggedIn(user, backend='django.contrib.auth.backends.ModelBackend')

    def test_should_have_username_field(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        form = response.context_data['form']
        UserModel = get_user_model()
        username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        self.assertEqual(form.fields['username'].label, capfirst(username_field.verbose_name))
