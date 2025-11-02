import os
import requests

import sys

action_id = sys.argv[1]

data = {"action_id": int(action_id)}

port = os.environ.get("PORT", "8080")

requests.post(f"http://localhost:{port}/actions_process", params=data)
