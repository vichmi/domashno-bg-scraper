import requests
import os
from lxml import html
from getpass import getpass
import time

url = "http://domashno.bg/"
loginurl = "http://domashno.bg/login"

USERNAME = input('Enter your email: ')
PASSWORD = getpass('Enter your password: ')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'origin': 'https://domashno.bg', 'referer': 'https://domashno.bg/login'
}

s = requests.session()

result = s.get(loginurl)
tree = html.fromstring(result.text)
authentication_token = tree.xpath("//input[@name='_token']/@value")[0]

payload = {
    '_token': authentication_token,
    'email': USERNAME,
    'password': PASSWORD
}

login_req = s.post(loginurl, headers=HEADERS, data=payload)

print('1. Maths \n2. Physics \n3. Chemistry')
subject = input('Enter the number of the subjects above: ')

while subject == (not'1' or not'2' or not'3'):
    print('Invalid subject')
    print()
    print('1. Maths \n2. Physics \n3. Chemistry')
    subject = input('Enter the number of the subjects above: ')

if subject == '1': subject = 'matematika'
if subject == '2': subject = 'fizika'
if subject == '3': subject = 'himiq'

result = s.get(f'https://domashno.bg/{subject}')
tree = html.fromstring(result.content)
classes = tree.xpath('//*[@class="media-body"]/div[@class="media mt-3"]/img[@class="mr-3"]/@alt')
print()
for i in range(0, len(classes)):
    classes[i] = classes[i].split(' ')[0]
    print(f'{i}. {classes[i]} grade. \n')

grade_index = input('Enter the number of the grade: ')

books_href = tree.xpath(f'//*[@class="media-body"]/div[{int(grade_index)+1}]/div[@class="media-body"]/div/a/@href')
books_text = tree.xpath(f'//*[@class="media-body"]/div[{int(grade_index)+1}]/div[@class="media-body"]/div/a/img/@alt')
print()
for i in range(0, len(books_href)):
    books_href[i] = books_href[i].split('/')[5]
    print(f'{i}. {books_text[i]}')

book = input('Enter the number of the book: ')

result = s.get(f'https://domashno.bg/{subject}/{classes[int(grade_index)]}/{books_href[int(book)]}/uroci/')
tree = html.fromstring(result.content)
units = tree.xpath('//*[@id="content"]/div[@class="container py-3 body-width"]/div[@class="row"]/div[@class="col-3"]/select[@class="form-control"]/option/@value')

if not os.path.exists(f'./units/{books_text[int(book)]}'): os.makedirs(f'./units/{books_text[int(book)]}')

print()
print('0. All units \n1. One unit')
exact_unit = input('Enter the number of your option: ')

while exact_unit == (not'0' or not'1'):
    print('Invalid input')
    print()
    print('0. All problems \n1. One problem')
    exact_unit = input('Enter the number of your option: ')

if exact_unit == '0':
    for unit in units:
        result = s.get(f'https://domashno.bg/{subject}/{classes[int(grade_index)]}/{books_href[int(book)]}/uroci/{unit}/zadachi')
        tree = html.fromstring(result.content)
        problems = tree.xpath('//*[@id="problems"]/ul/li/a/text()')
        if not os.path.exists(f'./units/{books_text[int(book)]}/{unit}'): os.makedirs(f'./units/{books_text[int(book)]}/{unit}')
        time.sleep(15)
        for problem in problems:
            exercise = s.get(f'https://domashno.bg/zadacha?p={subject}&k={classes[int(grade_index)]}&i={books_href[int(book)]}&u={unit}&z={problem}', headers=HEADERS)
            if exercise.status_code == 200:
                f = open(f'./units/{books_text[int(book)]}/{unit}/Problem {problem}.jpg', 'wb')
                f.write(exercise.content)
                f.close()
                time.sleep(20)
else:
    unit = input('Type the number of the unit')
    result = s.get(f'https://domashno.bg/{subject}/{classes[int(grade_index)]}/{books_href[int(book)]}/uroci/{unit}/zadachi')
    tree = html.fromstring(result.content)
    print()
    print('0. All problems \n1. A single problem')
    exact_problem = input('Enter the number of your option: ')
    problems = tree.xpath('//*[@id="problems"]/ul/li/a/text()')
    os.makedirs(f'./units/{books_text[int(book)]}/{unit}')
    while exact_problem == (not'0' or not'1'):
        print('Invalid input')
        print()
        print('0. All problems \n1. One problem')
        exact_problem = input('Enter the number of your option: ')

    if exact_problem == '0':
        for problem in problems:
            exercise = s.get(f'https://domashno.bg/zadacha?p={subject}&k={classes[int(grade_index)]}&i={books_href[int(book)]}&u={unit}&z={problem}', headers=HEADERS)
            if exercise.status_code == 200:
                f = open(f'./units/{books_text[int(book)]}/{unit}/Problem {problem}.jpg', 'wb')
                f.write(exercise.content)
                f.close()
    else:
        problem = input('Enter the number of the problem')
        exercise = s.get(f'https://domashno.bg/zadacha?p={subject}&k={classes[int(grade_index)]}&i={books_href[int(book)]}&u={unit}&z={problem}', headers=HEADERS)
        if exercise.status_code == 200:
            f = open(f'./units/{books_text[int(book)]}/{unit}/Problem {problem}.jpg', 'wb')
            f.write(exercise.content)
            f.close()