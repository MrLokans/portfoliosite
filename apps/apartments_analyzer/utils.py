USER_PROFILE_BASE_URL = "https://profile.onliner.by/user/"


def construct_onliner_user_url(user_id):
    return USER_PROFILE_BASE_URL + str(user_id)
