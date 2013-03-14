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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import forms as auth_forms, authenticate, get_user_model


class RegisterForm(auth_forms.UserCreationForm):
    class Meta():
        model = get_user_model()
        fields = [get_user_model().USERNAME_FIELD] + get_user_model().REQUIRED_FIELDS

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()
        if UserModel.USERNAME_FIELD != 'username':
            del self.fields['username']


class LoginForm(auth_forms.AuthenticationForm):
    pass
