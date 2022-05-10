from hashlib import new
import requests
import argparse
from datetime import datetime

def get_base_url():
    parser = argparse.ArgumentParser(description='Test this Flask api')
    parser.add_argument(
        'url',
        metavar='-u',
        type=str,
        nargs='?',
        help='the host url to test',
        default='http://127.0.0.1:5000/'
        )

    base_url = parser.parse_args().url

    if base_url[-1] == '/':
        base_url = base_url[:-1]
    if base_url[:4] != 'http':
        raise parser.error('is the url http:// or https:// ?')
    
    return base_url

def test(url, method, response_code, json=None):
    url = get_base_url() + url
    print(f'Testing URL: {url}')
    
    switch = {
        'get' : requests.get,
        'put' : requests.put,
        'post' : requests.post,
        'patch' : requests.patch,
        'delete' : requests.delete
    }

    r = switch[method](url, json=json)

    print(f'Desired Code: {response_code}')
    print(f'Actual Code: {r.status_code}')

    if r.status_code == response_code:
        print('Success!\n')
    else:
        print('Failed!\n')
        raise Exception(f'{url} provided the wrong response:\n{r}')
    
    return r.json()


# The basic request URL - http://127.0.0.1 by default
base_url = get_base_url()

# create a new person
new_person = {
    'first_name' : 'George',
    'last_name' : 'Harris',
    'nickname' : 'Madge'
}
# create a new place
new_place = {
    'name' : 'The Pub',
    'latitude' : '1.23',
    'longitude' : '3.21'
}
# create a new review
new_review = {
    'person_id' : 1,
    'place_id' : 1,
    'rating' : 6.9,
    'content' : "It ain't too bad, boii.",
    'date_created' : datetime.now().timestamp(),
    'date_modified' : datetime.now().timestamp()
}

# create a new person from provided json parameters
#test(f'/person', 'post', 200, json=new_person)
#test(f'/place', 'post', 200, json=new_place)
#test(f'/review', 'post', 200, json=new_review)

print('http://127.0.0.1:5000/person/create')
print('http://127.0.0.1:5000/place/create')
print('http://127.0.0.1:5000/review/create')

input('waiting....')

people = test(f'/person', 'get', 200)
places = test(f'/place', 'get', 200)
reviews = test(f'/review', 'get', 200)

print()
print(people)
print(places)
print(reviews)
print()

person = test(f'/person/1', 'get', 200)
place = test(f'/place/1', 'get', 200)
review = test(f'/review/1', 'get', 200)

print()
print(person)
print(place)
print(review)
print()

print('All good, G!')