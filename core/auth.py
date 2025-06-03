import hashlib
from typing import Optional

from fastapi import Response
from fastapi import Request
from passlib.handlers.sha2_crypt import sha512_crypt

from core.configs import settings

def try_hex_to_int(valor_hex: str) -> int:
    """
    Tenta converter valor hexadecimal para decimal
    """
    try:
        return int(valor_hex, 16)
    except:
        return 0


def __gerar_hash_cookie(texto: str) -> str:
    """
    Gerar hash de uma string
    """
    texto = settings.SALTY + str(texto) + 'CRIPTO'
    return hashlib.sha512(texto.encode('utf-8')).hexdigest()
    '''
    1. texto.encode('utf-8')
    Converte a string "texto" em uma sequência de bytes, usando a codificação UTF-8. 

    2. hashlib.sha512(...)
    Cria um objeto de hash utilizando o algoritmo SHA-512, que é uma função de hash 
    criptográfico da família SHA-2, transforma o "texto" em criptografia fixa de (64 bytes).

    3. .hexdigest()
    Converte o resumo gerado (em bytes) em uma representação hexadecimal legível: 
    uma string com 128 caracteres (cada byte vira dois dígitos hexadecimais). 
    '''


def set_auth(response: Response, membro_id: int) -> None:
    """
    Gerar cookie de autenticação do usuário logado ("auth_cookie")
    """
    # Gerar "SALTY" como membro_id Banco de Dados
    valor_hash: str = __gerar_hash_cookie(str(membro_id))

    # Gerar o valor hexadecimal do membro_id e pega somente a parte que nos interessa
    membro_id_hexadecimal: str = hex(membro_id)[2:]

    # Montar o valor do token (id_em_hexadecimal + . + hash)
    valor: str = membro_id_hexadecimal + '.' + valor_hash

    response.set_cookie(key=settings.AUTH_COOKIE_NAME, value=valor, httponly=True) # ("auth_cookie")
    '''
    Criar cookie HTTP no navegador do cliente a partir de uma resposta HTTP gerada pelo 
    servidor. Esse cookie é utilizado para autenticar o usuário nas requisições futuras.

    1. key=settings.AUTH_COOKIE_NAME: Define o nome do cookie, que está vindo de configs.py 
    2. value=valor: Define o valor do cookie (token)
    3. httponly=True:	Torna o cookie inacessível via JavaScript no navegador.
    '''


def gerar_hash_senha(senha: str) -> str:
    """
    Gerar hash (texto/senha)
    """
    hash_senha: str = sha512_crypt.hash(senha, rounds=123_456)

    return hash_senha


def verificar_hash_senha(senha: str , hash_senha: str) -> bool:
    """
    Verificar hash (texto/senha) contido no Banco de Dados
    """
    return sha512_crypt.verify(secret=senha, hash=hash_senha)


def get_membro_id(request: Request) -> Optional[int]:
    """
    Recupera o membro_id do cookie ("auth_cookie")
    """
    # Verifica se o cookie de autenticação existe ("auth_cookie")
    if settings.AUTH_COOKIE_NAME not in request.cookies:
        return None
    
    # Extrai o cookie ("auth_cookie")
    valor = request.cookies[settings.AUTH_COOKIE_NAME]

    # Separa as partes através do ponto
    partes = valor.split('.')

    # pegar a parte correspondente ao membro_id
    membro_id_hexadecimal: str = partes[0]

    # Converte de hexadecimal para numero decimal
    membro_id_decimal: int = try_hex_to_int(membro_id_hexadecimal)

    # Gerar "SALTY" como membro_id Banco de Dados
    check_valor_hash: str = __gerar_hash_cookie(membro_id_decimal)

    # adiciona o hexadecimal do membro_id e o ponto
    check_valor_hash = membro_id_hexadecimal + '.' + check_valor_hash
    
    # Se "valor" do hash for igual ao cookie ("auth_cookie")
    if valor != check_valor_hash:
        print('Alerta: Valor de cookie inválido.')
        return None
    
    return membro_id_decimal # id do membro usuário logado


def unset_auth(response: Response):
    """
    Função que remove o cookie ("auth_cookie") quando "logout"
    """
    response.delete_cookie(settings.AUTH_COOKIE_NAME)

