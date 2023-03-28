from twitter_agent import TwitterAgent
from components.config import Config


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

 
def grab_tweets(usernames: List[str], target_filename):
    # To set your environment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    # bearer_token = os.environ.get("BEARER_TOKEN")
    # agent = TwitterAgent(bearer_token)
    # usernames = [u['username'] for u in users['users']] 

    twitter_bearer_token = Config.TWITTER_BEARER_TOKEN
    agent = TwitterAgent(twitter_bearer_token)
    with open(target_filename, 'a') as target:
        for event in grab_user_tweets(agent, usernames):
            target.write(f'{event:s}\n')

def main():
    # users_filename = os.environ.get("USERS_FILENAME") or 'users.json'
    users_filename = Config.TWITTER_USERS_FILENAME
    target = Config.TWITTER_TARGET    
    with open(users_filename, 'r') as source:
        users = json.load(source)
        usernames = [u['username'] for u in users['users']]
        grab_tweets(usernames, )
        
