import os
from pathlib import Path
import json
from typing import Dict, List
import requests

from components.core import Metadata, TreeStore
from components.helpers import get_resource_identifier

IDENTIFIER = "twitter"

class TwitterAgent:
    def __init__(self, bearer_token: str) -> None:
        self._bearer_token = bearer_token
        
    @property
    def bearer_token(self) -> str:
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
                f"Request returned an error: {response.status_code} {response.text}"
                )
        return response.json()


def grab_user_tweets(agent: TwitterAgent, usernames: List[str]):
    url_user_info = agent.create_url_user_info(usernames)
    params = agent.get_params()
    try:
        response = agent.connect_to_endpoint(url_user_info, params)
        user_info = response['data']
        for this_user in user_info:
            event = {}
            event['user'] = this_user
            user_id = this_user['id']
            url_user_tweets = agent.create_url_user_tweets(user_id)
            response = agent.connect_to_endpoint(url_user_tweets, {})
            # user_data = 
            user_meta = response['meta']
            event['events'] = response['data']
            event['metadata'] = response['meta']
            yield json.dumps(event)
    except Exception as message:
        print(str(message)) 


# def create(bearer_token_file: Path) -> None:
#     with open(bearer_token_file, 'w') as target:
#         print(f"You must edit {str(bearer_token_file):s} "
#               "and replace the default token "
#               "with a valid twitter bearer_token"
#              )
#         secrets = {'bearer_token': "112358132134"}
#         json.dump(secrets, target)
# 
# def get_secrets(secrets: Path) -> Dict[str, str]:
#     bearer_token_file = Path(secrets, 'twitter').with_suffix('.json')
#     if not bearer_token_file.exists():
#         create(bearer_token_file)
#     with open(bearer_token_file, 'r') as source:
#         secrets = json.load(source)
#     return secrets

def grab_tweets(
    agent: TwitterAgent,
    usernames: List[str], 
    store: TreeStore
    ):
    new_sample = store.new_sample()
    target_filename = get_resource_identifier(new_sample, 'tweets', '.json')
    with open(target_filename, 'w') as target:
        for event in grab_user_tweets(agent, usernames):
            target.write(f'{event:s}\n')

def run(twitter_home: Path, bearer_token: str) -> None:
    store = TreeStore(twitter_home, 'tweets_from_api')
    store.start()
    users_filename = get_resource_identifier(twitter_home, 'users', '.json')    
    with open(users_filename, 'r') as source:
        users = json.load(source)
        usernames = [u['username'] for u in users['users']]
        agent = TwitterAgent(bearer_token)        
        grab_tweets(agent, usernames, store)
    store.stop()         
