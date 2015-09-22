
from bs4 import BeautifulSoup
import keyring
import requests


username = "vcooley"


def login(s):
    keys = keyring.get_keyring()
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


def get_students(s):
    """
    Gets a list of links to students pages
    :param s:
    :return student href list:
    """
    url = "https://www.pythonanywhere.com/user/{}/consoles".format(username)
    r = s.get(url)
    soup = BeautifulSoup(r.text)
    students_li_items = soup.find_all('li', role='presentation')
    student_links = []
    for li in students_li_items:
        link = li.a['href']
        student_links.append(link)
    return student_links




def main():
    with requests.Session() as s:
        login(s)
