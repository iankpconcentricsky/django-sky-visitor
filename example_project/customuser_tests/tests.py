from django.contrib.auth import get_user_model
from normal_tests.tests import RegisterViewTest


class CustomUserRegisterViewTest(RegisterViewTest):

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