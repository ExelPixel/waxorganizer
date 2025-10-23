from requests_oauthlib import OAuth1Session

# discogs = OAuth1Session('client_key',
#                             client_secret='client_secret',
#                             resource_owner_key='resource_owner_key',
#                             resource_owner_secret='resource_owner_secret')
# url = 'https://api.twitter.com/1/account/settings.json'
# r = discogs.get(url)

discogs = OAuth1Session(
        OAuth oauth_consumer_key="your_consumer_key",
        oauth_nonce="random_string_or_timestamp",
        oauth_signature="your_consumer_secret&",
        oauth_signature_method="PLAINTEXT",
        oauth_timestamp="current_timestamp",
        oauth_callback="your_callback"
)
url = 'https://api.twitter.com/1/account/settings.json'
r = discogs.get(url)
