# coding=utf-8
import requests
import json
url = 'http://127.0.0.1:8000/domains'
# url = 'http://127.0.0.1:8002/async_sleep_in_thread'
# url = 'http://127.0.0.1:8003/'
data = {
  "domains": {
    "domains": [
      "baidu.com"
    ]
  },
  "query_info": {
    "site_name": True,
    "company_name": True,
    "company_type": True,
    "main_page": True,
    "site_license": True,
    "verify_time": True
  }
}
data = json.dumps(data)
res = requests.post(url, data)
print(res.content.decode())