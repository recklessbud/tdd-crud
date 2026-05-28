# # Would be caught — high entropy:
# aws_key = "AKIA2QH4FVIJ8NQ5FCTP"  # Real AWS key format
# token = "ghp_16C7e42F292c6912E7710c838347Ae178B4ab"  # GitHub PAT

# # Would be caught — matches regex patterns:
# private_key = "-----BEGIN PRIVATE KEY-----\nMII..."
# db_url = "postgresql://user:password@host/db"


# import hashlib
# import random

# token = random.random()

# user_input = input()
# eval(user_input)


# hashlib.md5(b"password").hexdigest()
