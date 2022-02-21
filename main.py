from acessar_mysql import ConnBase

conn = ConnBase()

def print_ultimo():
    # soccer
    regra, ult_ent = conn.ultima_entrada('Soccer rule')
    print(f"Data da última entrada: {ult_ent} para regra {regra}.")
    # Health
    regra, ult_ent = conn.ultima_entrada('Health rule')
    print(f"Data da última entrada: {ult_ent} para regra {regra}.")
    # Food
    regra, ult_ent = conn.ultima_entrada('Food rule')
    print(f"Data da última entrada: {ult_ent} para regra {regra}.")

def print_primeiro():
    # soccer
    regra, ult_ent = conn.primeira_entrada('Soccer rule')
    print(f"Data da última entrada: {ult_ent} para regra {regra}.")
    # Health
    regra, ult_ent = conn.primeira_entrada('Health rule')
    print(f"Data da última entrada: {ult_ent} para regra {regra}.")
    # Food
    regra, ult_ent = conn.primeira_entrada('Food rule')
    print(f"Data da última entrada: {ult_ent} para regra {regra}.")

def print_mais_longo():
    # soccer
    tamanho, regra = conn.tweet_mais_longo('Soccer rule')
    print(f"Tweet mais longo: {tamanho} para regra {regra}.")
    # Health
    tamanho, regra = conn.tweet_mais_longo('Health rule')
    print(f"Tweet mais longo: {tamanho} para regra {regra}.")
    # Food
    tamanho, regra = conn.tweet_mais_longo('Food rule')
    print(f"Tweet mais longo: {tamanho} para regra {regra}.")

def print_mais_curto():
    # soccer
    tamanho, regra = conn.tweet_mais_curto('Soccer rule')
    print(f"Tweet mais curto: {tamanho} para regra {regra}.")
    # Health
    tamanho, regra = conn.tweet_mais_curto('Health rule')
    print(f"Tweet mais curto: {tamanho} para regra {regra}.")
    # Food
    tamanho, regra = conn.tweet_mais_curto('Food rule')
    print(f"Tweet mais curto: {tamanho} para regra {regra}.")

if __name__ == "__main__":
    print_ultimo()
    print_primeiro()
    print_mais_longo()
    print_mais_curto()