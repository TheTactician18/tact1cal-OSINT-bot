import requests

def getInfoByIP(ip='127.0.0.1'):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{f}').json
        return(response)
    except requests.exceptions.ConnectionError:
        return("[!] ConnectionError")
