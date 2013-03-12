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


app_default_settings = vars()

def get_app_setting(s, d=None):
    """
    Returns the first instance of the setting `s` that can be found in the order of priority: end user setting, the default `d` passed into the function, the app default setting specified in this file
    """
    import sys
    from django.conf import settings
    global app_default_settings
    try:
        app_default = app_default_settings[s]
    except KeyError:
        pass
    return getattr(settings, s, d or app_default)
