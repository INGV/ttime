import json
from datetime import datetime

def completeErrorStruct(req, json_data):
    data = json.loads(json_data)
    data["instance"] = req.url
    data["type"] = ""
    data["request_submitted"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S UTC')
    data["version"] = "1.0"
    return json.dumps(data)