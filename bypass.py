import requests
import easyocr
from bs4 import BeautifulSoup

# Coleta a URL
url = ''
while url.count('http') == 0:
    url = input('Insira a URL desejada: ')

# Função para burlar o Captcha
def captcha_bypass(site):
    captcha, captcha_temp = None, None
    tentativa = requests.get(site)

    # Raspa os dados com a tag <img> do site
    soup = BeautifulSoup(tentativa.text, features="html.parser")
    possiveis_captchas = soup.find_all('img')

    # Filtra qual das <img> é realmente o Captcha
    for i in possiveis_captchas:
        if str(i).lower().count('captcha') > 0:
            captcha_temp = i
    # Caso não encontre (ou seja, precisa de uma update para a estrutura do site)
    if captcha_temp is None:
        print('[DEBUG] Erro ao recuperar imagem de Captcha')
        exit()

    # Formata a tag para apenas uma URL
    captcha = str(captcha_temp)[10: len(captcha_temp) - 3]

    # Abre a imagem e salva em um arquivo
    imagem = requests.get(captcha, stream=True)
    salvar = open('captcha.jpg', 'wb')
    for pixel in imagem.iter_content(1024):
        if not pixel:
            break
        salvar.write(pixel)
    salvar.close()

    # Utiliza uma I.A. para analisar a imagem (a precisão depende do nível de complexibilidade do captcha)
    leitor = easyocr.Reader(['pt'])
    captcha = leitor.readtext('captcha.jpg', detail=0)

    return captcha[0]


print(captcha_bypass(url))
