import os
import json

import requests

from components.config import Config


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
            user_data = 
            user_meta = response['meta']
            event['events'] = response['data']
            event['metadata'] = response['meta']
            yield json.dumps(event)
    except Exception as message:
        print(str(message)) 


def start(bearer_token_file: Path) -> None:
    with open(bearer_token_file, 'w') as target:
        print(f"You must edit {str(bearer_token_file):s} "
              "and replace the default token "
              "with a valid twitter bearer_token"
             )
        secrets = {'bearer_token': "112358132134"}
        json.dump(secrets, target)

def get_secrets(secrets: Path) -> Dict[str, str]:
    bearer_token_file = Path(secrets, 'twitter').with_suffix('.json')
    if not bearer_token_file.exists():
        start(bearer_token_file)
    with open(bearer_token_file, 'r') as source:
        secrets = json.load(bearer_token_file)
    return secrets

def grab_tweets(usernames: List[str], store: TreeStore):
    # To set your environment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    # bearer_token = os.environ.get("BEARER_TOKEN")
    # agent = TwitterAgent(bearer_token)
    # usernames = [u['username'] for u in users['users']] 

    secrets = get_secrets(fs.secrets)
    agent = TwitterAgent(secrets['bearer_token'])
    new_sample = store.new_sample()
    target_filename = Path(new_sample, 'tweets').with_suffix('.json')
    with open(target_filename, 'w') as target:
        for event in grab_user_tweets(agent, usernames):
            store.write(f'{event:s}\n')


def run():
    # users_filename = os.environ.get("USERS_FILENAME") or 'users.json'
    fs = Config.FILESYSTEM
    twitter_root = Path(fs.data, 'twitter')
    store = TreeStore(twitter, 'tweets_from_api')
    store.start()
    users_filename = Path(twitter_root, 'users.json')    
    with open(users_filename, 'r') as source:
        users = json.load(source)
        usernames = [u['username'] for u in users['users']]
        grab_tweets(usernames, store)
    store.stop()         
