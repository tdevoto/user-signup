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
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return EMAIL_RE.match(email)

def forms(user_username, username_error, password_error, verify_error, user_email, email_error):
	headers = ("<head>"
		"<title>Sign Up</title>"
		"<style type='text/css'>"
			".error {color: red}"
		"</style>"
		"</head>"

        "<h2>Signup</h2>")


	tables = ("<table>"
		"<tr>"
			"<td>Username</td>"
			"<td><input type='text' name='username' value='" + user_username + "'></input></td>"
			"<td class='error'>" + username_error + "</td>"
		"</tr>"

		"<tr>"
			"<td>Password</td>"
			"<td><input type='password' name='password'></input></td>"
			"<td class='error'>" + password_error + "</td>"
		"</tr>"

		"<tr>"
			"<td>Verify Password</td>"
			"<td><input type='password' name='password_verify'></input></td>"
			"<td class='error'>" + verify_error + "</td>"
		"</tr>"

		"<tr>"
			"<td>Email (optional)</td>"
			"<td><input type='text' name='email' value='" + user_email + "'></input></td>"
			"<td class='error'>" + email_error + "</td>"
		"</tr>"
	"</table>")

	submit_button = "<input type='submit'/>"

	form = headers + "<form method='post'>" + tables + submit_button + "</form>"

	return form

class MainHandler(webapp2.RequestHandler):
	def get(self):
		content = forms("", "", "", "", "", "")
		self.response.write(content)

        def post(self):
		errorcount = 0
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("password_verify")
		email = self.request.get("email")
		username_error = ""
		password_error = ""
		verify_error = ""
		email_error = ""

		if not username or not valid_username(username):
			username_error = "Username not valid."
			errorcount += 1
		if not password or not valid_password(password):
			password_error = "That's not a valid password."
			errorcount += 1
		if password != verify:
			verify_error = "The passwords don't match."
			errorcount += 1
		if  email != '' and not valid_email(email):
			email_error = "That's not a valid email address."
			errorcount += 1

		if errorcount > 0:
			content = forms(username, username_error, password_error, verify_error, email, email_error)
			self.response.write(content)
		else:
			self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
	def get(self):
		username = self.request.get("username")
		header = "<h2>Welcome, " + username + "!" + "</h2>"
		self.response.write(header)

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', Welcome)
], debug=True)
