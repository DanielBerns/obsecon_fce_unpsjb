import os
import json

import requests

class TwitterAgent:
    def __init__(self, bearer_token):
        self._bearer_token = bearer_token
        
    @property
    def bearer_token(self):
        return self._bearer_token

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r
    
    def create_url_user_info(self, usernames, userfields=None):
        # Specify the usernames that you want to lookup.
        # You can enter up to 100 comma-separated values    
        # User fields are adjustable, options include:
        # created_at, description, entities, id, location, name,
        # pinned_tweet_id, profile_image_url, protected,
        # public_metrics, url, username, verified, and withheld
        if userfields is None:
            userfields = ['created_at', 'description', 'id']
        csv_usernames = ','.join(usernames)
        csv_userfields = ','.join(userfields)
        arg_usernames = f"usernames={csv_usernames:s}"
        arg_userfields = f"user.fields={csv_userfields:s}"
        url = f"https://api.twitter.com/2/users/by?{arg_usernames:s}&{arg_userfields:s}"
        return url

    def get_params(self):
        # Tweet fields are adjustable.
        # Options include:
        # attachments, author_id, context_annotations,
        # conversation_id, created_at, entities, geo, id,
        # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
        # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
        # source, text, and withheld
        return {"tweet.fields": "created_at,geo,id"}
  
    def create_url_user_tweets(self, user_id):
        return f"https://api.twitter.com/2/users/{user_id}/tweets"

    def connect_to_endpoint(self, url, params):
        response = requests.request("GET", 
                                    url, 
                                    auth=lambda r: self.bearer_oauth(r), 
                                    params=params)
        if response.status_code != 200:
            print('HTTP Response Status Code', response.status_code)
            raise Exception(
                "Request returned an error: {response.status_code} {response.text}"
                )
        return response.json()

