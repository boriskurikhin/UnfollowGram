import requests
import json
from time import sleep
from random import randint
import sys

#all our URLs
url = 'https://www.instagram.com'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
followers_url = 'https://www.instagram.com/graphql/query/'

session = requests.Session()
userId = None

def get_followers():
    #try to log in
    logged_in = login()

    if not logged_in:
        print('Could not log in, check to see if credentials are valid. Or disable 2-step authentication.')
        sys.exit(0)

    # this is the query that browers seem to be using to fetch followers
    # we can maybe fetch # of followers and just set 'first' to that
    query = { 
        'id' : userId,
        'include_reel': 'true'
        'fetch_mutual': 'true',
        'first': randint(20, 50)
    }

    #let's get followers
    response = session.get(followers_url, params={ })
    


    

def login():

    #make it look like we're logging in from Chrome
    session.headers.update({
        'Connection': 'keep-alive',
        'X-Instagram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest'
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    })

    #extact csrf token
    response = session.get(url)
    csrf_token = response.cookies['csrftoken']
    
    login = {}

    #add it to the session
    session.headers.update({ 'X-CSRFToken': csrf_token })

    #load credentials from JSON file
    try:
        with open('login.json', 'r') as credentials:
            login = json.loads(credentials.read())
    except Exception:
        print('Looks like you don\'t have a "login.json" - create one now & re-start')

    #sleep a random amount of time so they'll think we're a human
    sleep(randint(3, 7))

    response = session.post(login_url, data=login, allow_redirects=True)
    
    #let's hope it works bois
    great_success = json.loads(response.text)
    
    #update csrftoken once again
    csrf_token = great_success.cookies['csrftoken']

    #get the user id, we'll need this to get our followers
    userId = great_success['userId']
    session.headers.update({ 'X-CSRFToken': csrf_token })
    
    return great_success['authenticated']


login()