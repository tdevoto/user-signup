#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import cgi

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""
class Index(webapp2.RequestHandler):


    def get(self):

        user_form = """
        <form action="/add" method="post">
            <label>
                Username
                <input type="text" name="username"/>

            </label>
            <br>
            <label>
                Password
                <input type="text" name="password"/>

            </label>
            <br>
            <label>
                Verify Password
                <input type="text" name="verify"/>

            </label>
            <br>
            <label>
                Email (optional)
                <input type="text" name="email"/>

            </label>
            <br>
            <input type="submit" value="Submit"/>
        </form>
        """
        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = "<p class='error'>" + error_esc + "</p>"
        else:
            error_element = ""

        # combine all the pieces to build the content of our response
        content = page_header + user_form + error_element
        self.response.write(content)

class Sub(webapp2.RequestHandler):


    def post(self):
        edit_header = "<h3>Welcome</h3>"
        # look inside the request to figure out what the user typed
        user = self.request.get("username")


        content = edit_header + user
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', Sub)
], debug=True)
