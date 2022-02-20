class Tweet():

    def __init__(self, user_id, texto_do_tweet, regra) -> None:
        self.id_usuario_twitter = user_id
        self.texto = texto_do_tweet
        self.regra = regra

    def retorno_dicionario(self):
        return {
            "userid": self.id_usuario_twitter,
            "texto": self.texto,
            "regra": self.regra
        }