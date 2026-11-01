import requests

def getInfoByIP(ip='127.0.0.1'):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        return response
    except requests.exceptions.ConnectionError:
        return {"status": "fail", "message": "Connection Error"}