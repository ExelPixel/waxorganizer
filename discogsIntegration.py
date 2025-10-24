import requests as rq
from requests_oauthlib import OAuth1Session

def OAuth():
    DISCOGS_CONSUMER_KEY = 'sFmZpGzWbubyXcFDLyfz'
    DISCOGS_CONSUMER_SECRET = 'OaoOJooRfYzAldNRrHBLsdLeMBPjwacN'
    DISCOGS_REQUEST_TOKEN_URL = 'https://api.discogs.com/oauth/request_token'
    DISCOGS_AUTHORIZE_URL = 'https://www.discogs.com/oauth/authorize'
    DISCOGS_ACCESS_TOKEN_URL = 'https://api.discogs.com/oauth/access_token'

    discogs = OAuth1Session(
        client_key=DISCOGS_CONSUMER_KEY,
        client_secret=DISCOGS_CONSUMER_SECRET,
    )

    request_token = discogs.fetch_request_token(DISCOGS_REQUEST_TOKEN_URL)

    authorization_url = discogs.authorization_url(DISCOGS_AUTHORIZE_URL)
    print(f'Please go to {authorization_url} and authorize access')

    # verifier = input('Paste the verifier code here: ')
    verifier = "uyCFdOkpPj"

    discogs = OAuth1Session(
        client_key=DISCOGS_CONSUMER_KEY,
        client_secret=DISCOGS_CONSUMER_SECRET,
        resource_owner_key=request_token['oauth_token'],
        resource_owner_secret=request_token['oauth_token_secret'],
        verifier=verifier
    )
    return discogs.fetch_access_token(DISCOGS_ACCESS_TOKEN_URL)

accessToken = OAuth()

def getRecordName(catNum):
    result = rq.get(f"https://api.discogs.com/database/search?catno={catNum}&type=release")
    return result
