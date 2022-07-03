import urllib.parse
from bs4 import BeautifulSoup as bs
from app_globals import base_url, s
import getpass
import base64


def login():
    username = input("Username [%s]:" % getpass.getuser())
    password = getpass.getpass()
    login_form = base_url + "Authentication/Login"
    soup = bs(s.get(login_form).content, 'html.parser')
    request_verification_token = soup.findAll(
        attrs={'name': '__RequestVerificationToken'})[1]['value']
    login_url = login_form + "/DoLogin"
    login_data = "__RequestVerificationToken=" + request_verification_token + "&LoginInfo=" + urllib.parse.quote(
        '{"Type":"StandardLogin","Credentials":{"Username":"' + b64(username) + '","Password":"' + b64(password) + '"}}')
    page = s.post(login_url, data=login_data, headers={
                  'Content-Type': 'application/x-www-form-urlencoded'})
    print('login status code:')
    print(page.status_code)


def switch_profile():
    bea_switch_url = base_url + "/inside.asp?mode=proxyswitch&action=switchcontext&src=0&eid=WP-24i5hVk9ROLerhkWkZOT8B5w-3D-3D-247laxErw8wPT615aIg-2FJgpIeXnaHtC7FQh63PaN7U-2Fbg-3D"
    page = s.get(bea_switch_url)
    print('bea switch status code:')
    print(page.status_code)


def b64(input_string):
    return base64.b64encode(input_string.encode('ascii')).decode('ascii')
