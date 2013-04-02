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

from django import forms
from django.forms import widgets


class Html5EmailInput(widgets.Input):
    input_type = 'email'


class PasswordRulesField(forms.CharField):
    DEFAULT_MIN_LENGTH = 8

    # TODO: Add more validators. And move them to validators.py

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        if not min_length:
            min_length = self.DEFAULT_MIN_LENGTH
        if not kwargs.get('widget', None):
            kwargs['widget'] = forms.PasswordInput
        super(PasswordRulesField, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        if value is None or len(value) < self.min_length:
            raise forms.ValidationError("Password must be at least %d characters long." % self.min_length)
        return super(PasswordRulesField, self).clean(value)
