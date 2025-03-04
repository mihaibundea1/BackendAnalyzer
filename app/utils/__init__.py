from .blackblaze import initialize_b2

def initialize_blackblaze(APPLICATION_KEY_ID, APPLICATION_KEY):
    app_key_id = APPLICATION_KEY_ID
    app_key = APPLICATION_KEY
    return initialize_b2(app_key_id, app_key)