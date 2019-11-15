import requests
import pandas as pd
url = "https://api.hypr.cl/raw/"
headers = {
    'x-api-key': "iQ0WKQlv3a7VqVSKG6BlE9IQ88bUYQws6UZLRs1B",
    'time_start': "2019-08-01T12:00:00Z",
    'time_stop': "2019-08-01T12:01:00Z",
    'Accept': "*/station*",
    'Cache-Control': "no-cache",
    'Host': "api.hypr.cl",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "0",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}
response = requests.request("POST", url, headers=headers)
# print(response.text)
df = pd.read_json(response.text)
print(df.head())
