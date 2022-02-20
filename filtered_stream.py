from decouple import config
import requests 
import json
from acessar_mysql import ConnBase

class FilteredStream():

    def __init__(self, rules):
        # pega as credenciais do API do twitter
        self.api_key = config('TWITTER_API_KEY')
        self.secret_key = config('TWITTER_API_SECRET_KEY')
        self.bearer_token = config('TWITTER_BEARER_TOKEN')

        # regras que definem a busca nos tweets
        self.rules = rules

    # autorização para acessar os dados via API
    def bearer_auth(self, r):
        r.headers["Authorization"] = f'Bearer {self.bearer_token}'
        r.headers["User-Agent"] = "v2FilteredStreamPython"

        return r

    def _get_regras(self):
        # busca por regras já existentes e retorna um arquivo json
        resposta = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_auth
        )

        if resposta.status_code != 200:
            # code 200 html - ok
            raise Exception(
                f"Cannot get rules (HTTP {resposta.status_code}): {resposta.text}"
            )
        #print(json.dumps(resposta.json()))

        return resposta.json()

    def _deletar_regras(self, regras):
        # pega as regras do get_regras e as deleta
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
                
    
    def _set_rules(self):
        # define novas regras
        sample_rules = self.rules

        payload = {"add": sample_rules}

        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_auth,
            json=payload
        )

        if response.status_code != 201: # create - ok
            raise Exception(
                f"Cannot add rules (HTTP {response.status_code}): {response.text}"
            )
        
    def _get_stream(self):
        # se conecta e pega a stream de dados
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream",
            auth=self.bearer_auth,
            stream=True
        )

        if response.status_code != 200:
            raise Exception(
                f"Cannot get stream (HTTP({response.status_code}): {response.text}"
            )

        conn = ConnBase() # instancia para conectar ao DB
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)

                # dados que serão salvos no DB - userid, texto e regra
                user_id = json_response["data"]["id"]
                tweet_text = json_response["data"]["text"]
                regra = json_response["matching_rules"][0]["tag"]

                # salva dados acima na tabela
                conn.insert_to_table(
                    user_id,
                    tweet_text,
                    regra
                )

    def go(self):
        # test only
        past_rules = self._get_regras()
        self._deletar_regras(past_rules)
        self._set_rules()
        self._get_stream()

if __name__=="__main__":
    rules = [
        {"value": "Futebol lang:pt", "tag": "Soccer rule"},
        {"value": "Saúde lang:pt", "tag": "Health rule"},
        {"value": "Comida lang:pt", "tag": "Food rule"}
    ]

    # faz todo processo de coletar da API e salvar no DB
    fsi = FilteredStream(rules)
    fsi.go()