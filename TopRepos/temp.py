import requests
url = 'https://api.github.com/orgs/microsoft/repos?page=1&per_page=100'
response = requests.get(url)
link = response.headers.get('link', None)
if link is not None:
    print(link)