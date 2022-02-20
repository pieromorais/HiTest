from decouple import config
import requests 
import json

class FilteredStream():

    def __init__(self, rules):
        self.api_key = config('TWITTER_API_KEY')
        self.secret_key = config('TWITTER_API_SECRET_KEY')
        self.bearer_token = config('TWITTER_BEARER_TOKEN')

        self.rules = rules

    def bearer_auth(self, r):
        r.headers["Authorization"] = f'Bearer {self.bearer_token}'
        r.headers["User-Agent"] = "v2FilteredStreamPython"

        return r

    def get_regras(self):

        resposta = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_auth
        )

        if resposta.status_code != 200:
            # code 200 html - ok
            raise Exception(
                f"Cannot get rules (HTTP {resposta.status_code}): {resposta.text}"
            )
        print(json.dumps(resposta.json()))

        return resposta.json()

    def deletar_regras(self, regras):
        if regras is None or "data" not in regras:
            return None
        ids = list(map(lambda regra: regra["id"], regras["data"]))
        
        payload = {"delete": {"ids": ids}}

        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_auth,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(
                f"Não foi possível deletar regras (HTTP {response.status_code}): {response.text}"
            )
        
        print(json.dumps(response.json()))
        
    
    def set_rules(self):

        print(type(self.rules))
        sample_rules = self.rules
        print(type(self.rules))

        payload = {"add": sample_rules}

        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_auth,
            json=payload
        )

        if response.status_code != 201:
            raise Exception(
                f"Cannot add rules (HTTP {response.status_code}): {response.text}"
            )
        
        print(json.dumps(response.json()))

    def get_stream(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream",
            auth=self.bearer_auth,
            stream=True
        )

        if response.status_code != 200:
            raise Exception(
                f"Cannot get stream (HTTP({response.status_code}): {response.text}"
            )

        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                print(json.dumps(json_response, indent=4, sort_keys=True))

    def go(self):
        # test only
        past_rules = self.get_regras()
        self.deletar_regras(past_rules)
        self.set_rules()
        self.get_stream()

if __name__=="__main__":
    rules = [
        {"value": "Futebol lang:pt", "tag": "Soccer rule"},
        {"value": "Saúde lang:pt", "tag": "Health rule"},
        {"value": "Comida lang:pt", "tag": "Food rule"}
    ]

    fsi = FilteredStream(rules)
    fsi.go()