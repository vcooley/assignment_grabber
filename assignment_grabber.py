__author__ = 'Vince'

from bs4 import BeautifulSoup
import keyring
import requests


def login(s):
    keys = keyring.get_keyring()
    username = "vcooley"
    password = keys.get_password("pythonanywhere", username)

    url = "https://www.pythonanywhere.com/login/"
    header = {"Referer": url}
    s.get(url)
    csrftoken = s.cookies['csrftoken']

    payload = {"username": username,
               "password": password,
               "csrfmiddlewaretoken": csrftoken
               }
    r = s.post(url, data=payload, headers=header)

soup =

def main():
    with requests.Session() as s:
        login(s)