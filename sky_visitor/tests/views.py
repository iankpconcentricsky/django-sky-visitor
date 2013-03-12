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
from django.contrib.auth.tests import skipIfCustomUser
from django.test.utils import override_settings
from sky_visitor.tests.base import SkyVisitorTestCase
from sky_visitor.tests.utils import skipUnlessCustomUser


class SkyVisitorViewsTestCase(SkyVisitorTestCase):

    def setUp(self):
        super(SkyVisitorViewsTestCase, self).setUp()


class RegisterViewBase(object):
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


@skipIfCustomUser
class RegisterViewTest(RegisterViewBase, SkyVisitorViewsTestCase):
    pass


@override_settings(AUTH_USER_MODEL='auth.CustomUser')
class CustomUserRegisterViewTest(RegisterViewBase, SkyVisitorViewsTestCase):

    def get_test_data(self):
        data = {
            'email': 'registeruser@example.com',
            'date_of_birth': '1976-11-08',
            'password1': 'password',
            'password2': 'password',
        }
        return data

    def test_registration_should_fail_on_duplicate_email(self):
        UserModel = get_user_model()
        testuser_email = 'testuser1@example.com'
        data1 = self.get_test_data()
        data1['email'] = testuser_email
        response1 = self.client.post(self.view_url, data=data1, follow=True)
        self.assertEqual(response1.status_code, 200)
        # Test user should exist
        self.assertEqual(UserModel._default_manager.filter(**{UserModel.USERNAME_FIELD: testuser_email}).count(), 1)

        data2 = data1
        response2 = self.client.post(self.view_url, data=data2, follow=True)
        self.assertEqual(response2.status_code, 200)
        form = response2.context_data['form']
        # Form should have errors for the duplicate email
        self.assertEqual(len(form.errors), 1)
        self.assertIn('email', form.errors)

        # Test user should only be in the database one time
        self.assertEqual(UserModel._default_manager.filter(**{UserModel.USERNAME_FIELD: testuser_email}).count(), 1)