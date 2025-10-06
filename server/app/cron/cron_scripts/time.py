import requests

import sys


action_id = sys.argv[1]

data = {"action_id": int(action_id)}

requests.post("http://localhost:8080/actions_process", params=data)
