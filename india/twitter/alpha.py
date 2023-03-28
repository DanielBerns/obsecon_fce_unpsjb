import twitter as tw
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

t = tw.Twitter(auth=tw.OAuth2(bearer_token=bearer_token))
    
with open('users.json', 'r') as source:
    users_list = json.load(source)
    usernames = [u['username'] for u in users_list['users']]
    
# Get a particular friend's timeline
for name in usernames:
    t.statuses.user_timeline(screen_name=name)
