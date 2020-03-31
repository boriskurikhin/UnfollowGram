import requests
import json
from time import sleep
import random
import sys

#all our URLs
url = 'https://www.instagram.com'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
followers_url = 'https://www.instagram.com/graphql/query/'

session = requests.Session()
query_hash = 'c76146de99bb02f6415203be841dd25a' #some sort of md5 hash used for follower lookup (seems cosntant)

def get_followers():
    #try to log in
    logged_in = login()

    if not logged_in['success']:
        print('Could not log in, check to see if credentials are valid. Or disable 2-step authentication.')
        sys.exit(0)

    # this is the query that browers seem to be using to fetch followers
    # we can maybe fetch # of followers and just set 'first' to that
    query = { 
        'id' : logged_in['userId'],
        'include_reel': False,
        'fetch_mutual': False,
        'first': random.randint(100, 200) #does my query_hash only work with 24? we'll find out, UPDATE: guess not
    }

    followers = []
    
    #iteratively add followers
    hasNextPage = True
    offset = ''

    while hasNextPage:
        #sleep, so we dont' seem like a machine
        sleep(random.uniform(0, 2)) 

        #insert offset
        if len(offset) > 0:
            query['after'] = offset

        response = session.get(followers_url, params={'query_hash': query_hash, 'variables': json.dumps(query)})
        response_data = json.loads(response.text)

        for follower in response_data['data']['user']['edge_followed_by']['edges']:
            followers.append(follower['node']['username'])

        print ('retrieved a bunch of followers...')

        hasNextPage = response_data['data']['user']['edge_followed_by']['page_info']['has_next_page']
        offset  = response_data['data']['user']['edge_followed_by']['page_info']['end_cursor']

    #write followers to file
    with open('followers.txt', 'w+') as ff:
        ff.write("\n".join(followers))

    return followers

def login():

    #make it look like we're logging in from Chrome
    session.headers.update({
        'Connection': 'keep-alive',
        'X-Instagram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    })

    # apparently this is important?
    session.cookies.update({
        'ig_pr': '1',
        'ig_vw': '1920',
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
    sleep(random.randint(3, 7))

    response = session.post(login_url, data=login, allow_redirects=True)
    
    #let's hope it works bois
    great_success = json.loads(response.text)
    
    #update csrftoken once again
    csrf_token = response.cookies['csrftoken']

    #get the user id, we'll need this to get our followers
    userId = great_success['userId']
    session.headers.update({ 'X-CSRFToken': csrf_token })

    #kind of important we have this
    assert userId is not None
    
    return {
        'success' : great_success['authenticated'],
        'userId': userId
    }

get_followers()