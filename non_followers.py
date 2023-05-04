import sys
from time import sleep
from instagram_private_api import Client, ClientCompatPatch

def login(username, password):
    try:
        # Log in to Instagram API using provided credentials
        api = Client(username, password)
        return api
    except Exception as e:
        print(f"Error logging in: {e}")
        sys.exit(1)

def get_non_followers(api):
    # Get authenticated user ID
    user_id = api.authenticated_user_id
    
    # Generate a unique rank token
    rank_token = Client.generate_uuid()

    # Get followers and followings of the authenticated user
    followers_response = api.user_followers(user_id, rank_token=rank_token)
    followers = {user['pk'] for user in followers_response['users']}
    
    followings_response = api.user_following(user_id, rank_token=rank_token)
    followings = {user['pk']: user for user in followings_response['users']}

    # Get IDs of non-followers by taking the difference between followings and followers
    non_follower_ids = followings.keys() - followers
    
    # Get non-followers' information
    non_followers = [followings[user_id] for user_id in non_follower_ids]

    return non_followers

def unfollow_users(api, selected_users):
    # Unfollow the selected users
    for user_id in selected_users:
        api.friendships_destroy(user_id)