
from bs4 import BeautifulSoup
import keyring
import os
import requests


teacher_username = "vcooley"


def login(s):
    keys = keyring.get_keyring()
    password = keys.get_password("pythonanywhere", teacher_username)

    url = "https://www.pythonanywhere.com/login/"
    header = {"Referer": url}
    s.get(url)
    csrftoken = s.cookies['csrftoken']

    payload = {"username": teacher_username,
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
    url = "https://www.pythonanywhere.com/user/{}/consoles".format(teacher_username)
    r = s.get(url)
    soup = BeautifulSoup(r.text)
    students_li_items = soup.find_all('li', role='presentation')
    student_usernames = []
    for li in students_li_items:
        link = li.a['href']
        user = link[6:-1]
        student_usernames.append(user)
    return student_usernames


def get_file(s, user, filename, path='/', root=None):
    """
    Takes a session object, a username, a filename, the path to the file,
    and the root if it is not the standard path the user finds when navigating to his files tab.
    Returns a file if it is found or None if it is not found.
    :param s:
    :param user:
    :param filename:
    :param path:
    :param root:
    :return file or None:
    """
    if root is None:
        root = "/home/{}".format(user)
    url = "https://www.pythonanywhere.com/user/{user}/files{root}{path}{filename}".format(user=user,
                                                                                          root=root,
                                                                                          path=path,
                                                                                          filename=filename
                                                                                          )
    r = s.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return None


def save_assignments(s, assignment_name, user_list, assignment_path=None, file_path=None):
    """
    :param s: request.Session
    :param assignment_name: str
    :param user_list: list
    :return: None
    """
    if not assignment_path:
        assignment_path = '/'
    filename = assignment_name + ".py"
    local_user = os.getenv("USERNAME")
    if not file_path:
        file_path = "C://Users/{}/Documents/CompSci/{}".format(local_user, assignment_name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for student in user_list:
        file_as_str = get_file(s, student, filename, assignment_path)
        student_file_path = file_path + "/{}.py".format(student)
        if file_as_str:
            with open(student_file_path, "w") as assignment:
                assignment.write(file_as_str)


def prompt_for_info():
    assignment_name = input("Enter assignment name:")
    assignment_path = input("Enter assignment path (e.g. /homework/ or /practice/:")
    return assignment_name, assignment_path


def main():
    with requests.Session() as s:
        login(s)
        students = get_students(s)
        assignment, path = prompt_for_info()
        save_assignments(s, assignment, students)


if __name__ == "__main__":
    main()