import base64
from bs4 import BeautifulSoup
import hashlib
import random
import requests
import string

class Tesla:
    def __init__(self):
        self.login()
    
    def login(self):
        code_verifier = ''.join([random.choice(string.ascii_lowercase) for _ in range(86)]).encode()
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier).hexdigest().encode())
        params = {
            'client_id': "ownership",
            # 'code_challenge': code_challenge,
            # 'code_challenge_method': 'S256',
            'redirect_uri': 'https://www.tesla.com/teslaaccount/owner-xp/auth/callback',
            'response_type': 'code',
            'scope': 'offline_access openid ou_code email phone', # ou_code phone',
            'audience': 'https://ownership.tesla.com/',
            'locale': 'en-US',
            # 'login_hint': 'avatheavian@gmail.com'
        }
        response = requests.get('https://auth.tesla.com/oauth2/v1/authorize', params=params, headers={
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            'referer': 'https://www.tesla.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'macOS',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
            'upgrade-insecure-requests': '1',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded'
        })
        parser = BeautifulSoup(response.text, features="html.parser")
        hidden_fields = [i for i in parser.find_all('input') if i.get('type') == 'hidden']
        print(hidden_fields)
        
        params = {
            'client_id': 'ownership',
            # 'code_challenge': code_challenge,
            # 'code_challenge_method': 'S256',
            'redirect_uri': 'https://www.tesla.com/teslaaccount/owner-xp/auth/callback',
            'response_type': 'code',
            'scope': 'offline_access openid ou_code email phone',
            'audience': 'https://ownership.tesla.com/',
            'locale': 'en-US',
        }
        data = {
            # **{i.get('name'): i.get('value') for i in hidden_fields},
            'identity': 'avatheavian@gmail.com',
            'credential': '5baEheQHdzfEmzNpAKpTzpzDaTemCMnKo3nTk7HS',
            # '_phase': 'authenticate',
            # '_process': 1
        }
        response_post = requests.post(
            'https://auth.tesla.com/oauth2/v1/authorize',
            cookies=response.cookies,
            params=params,
            data=data,
            headers={
                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-user': '?1',
                'sec-ch-ua-platform': 'macOS',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-site',
                'upgrade-insecure-requests': '1',
                'accept-language': 'en-US,en;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'cache-control': 'max-age=0',
                'origin': 'https://auth.tesla.com',
                'content-type': 'application/x-www-form-urlencoded',
                'referer': f'https://auth.tesla.com/oauth2/v1/authorize?{"&".join([f"{urllib.parse.quote(k)}={urllib.parse.quote(v)}".replace("/", "%2F") for k,v in params.items()])}'
            },
            allow_redirects=False
        )
        # if response_post.status_code != 302:
        #     raise Exception(f"Failed to login to Tesla API: {response_post.text}")
            
        # loc = response_post.headers["Location"]
        # data = {
        #     "grant_type": "authorization_code",
        #     "client_id": "ownerapi",
        #     # "code": response_post.cookies['tesla-auth.sid'],
        #     "code": response.headers['set-cookie'].split(';')[0].replace('tesla-auth.sid=', '', 1),
        #     "code_verifier": code_verifier,
        #     "redirect_uri": "https://auth.tesla.com/void/callback"
        # }
        # response_final = requests.post(
        #     'https://auth.tesla.com/oauth2/v3/token',
        #     data=data
        # )
        import pdb; pdb.set_trace()
        print()