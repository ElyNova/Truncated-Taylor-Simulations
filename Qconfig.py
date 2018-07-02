import os
APItoken = "d5073a918e7711e2f6a1faac0bea8725fd9f09fe635418849779bbea18f2bd96070aa8000793ddc2d53177b711c1f85e978d7e2ee6a6ebcc2de4b9bb8ce55af4"
config = {
  "url": 'https://quantumexperience.ng.bluemix.net/api'
}

def update_token(token=APItoken):
    """Update the APItoken.
       :param token: The API token.(optional argument)
              If thisis set, it must be a string. The default value is None
    """
    global APItoken

    # If a token is given as an argument, use it.
    if token:
        APItoken = token
    else:
        # First check if APItoken is already set. If so, just use it.
        if APItoken:
            # Do nothing. The APItoken will override
            pass
        else:
            APItoken = os.getenv("IBMQE_API")
    assert (APItoken not in (None, '') and type(APItoken) is str), "Please set up a valid API access token. See Qconfig.py."

# Update the APItoken
update_token()
