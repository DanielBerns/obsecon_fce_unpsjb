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
        return {"tweet.fields": "created_at"}
  
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



# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

agent = TwitterAgent(bearer_token)

with open('users.json', 'r') as source,
    users = json.load(source)
    usernames = [u['username'] for u in users['users']] 
    url_user_info = agent.create_url_user_info(usernames)
    params = agent.get_params()
    response = agent.connect_to_endpoint(url_user_info, params)
    user_info = response['data']
    for this_user in user_info:
        print('*'*80)
        print('this_user')
        for key, value in this_user.items():
            print('    ', key, '-', value)
        print('-'*80)
        username = this_user['username']
        user_id = this_user['id']
        url_user_tweets = agent.create_url_user_tweets(user_id)
        response = agent.connect_to_endpoint(url_user_tweets, {})
        print('username', username, 'user_id', user_id)
        user_data = response['data']
        user_meta = response['meta']
        print('-'*80)
        for event in user_data:
            for key, value in event.items():
                print('   data[', key, ']  ', str(value))
            print('.'*80)
        for key, value in user_meta.items():
            print('   meta:', key, value)
        print('='*80)
