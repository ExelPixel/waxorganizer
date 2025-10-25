#!/usr/bin/env python
#
# This illustrates the call-flow required to complete an OAuth request
# against the discogs.com API, using python3-discogs-client libary.
# The script will download and save a single image and perform and
# an API search API as an example. See README.md for further documentation.

import sys

from dotenv import load_dotenv
import os

import discogs_client
from discogs_client.exceptions import HTTPError

def auth():

    load_dotenv("consumer.env")
    consumer_key = os.getenv("consumerKey")
    consumer_secret = os.getenv("consumerSecret")

    user_agent = "waxorganizer"

    discogsclient = discogs_client.Client(user_agent)

    discogsclient.set_consumer_key(consumer_key, consumer_secret)
    token, secret, url = discogsclient.get_authorize_url()

    print(" == Request Token == ")
    print(f"    * oauth_token        = {token}")
    print(f"    * oauth_token_secret = {secret}")
    print()

    print(f"Please browse to the following URL {url}")

    accepted = "n"
    while accepted.lower() == "n":
        print()
        accepted = input(f"Have you authorized me at {url} [y/n] :")

    oauth_verifier = input("Verification code : ")

    try:
        access_token, access_secret = discogsclient.get_access_token(oauth_verifier)
    except HTTPError:
        print("Unable to authenticate.")
        sys.exit(1)

    user = discogsclient.identity()

    print()
    print(" == User ==")
    print(f"    * username           = {user.username}")
    print(f"    * name               = {user.name}")
    print(" == Access Token ==")
    print(f"    * oauth_token        = {access_token}")
    print(f"    * oauth_token_secret = {access_secret}")
    print(" Authentication complete. Future requests will be signed with the above tokens.")

    return discogsclient

def getRecordName(catNumList):
    discogsclient = auth()

    for catNum in catNumList:
        search_results = discogsclient.search(catNum, type="release")
        print("\n== Search results for release_title=House For All ==")

        for release in search_results:
            # print(f"\n\t== discogs-id {release.id} ==")
            # print(f'\tArtist\t: {", ".join(artist.name for artist in release.artists)}')
            # print(f"\tTitle\t: {release.title}")
            # print(f"\tYear\t: {release.year}")
            # print(f'\tLabels\t: {", ".join(label.name for label in release.labels)}')
            return release.title
        
    return None
