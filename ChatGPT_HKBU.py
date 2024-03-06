import configparser
import requests


class HKBU_CHATGPT():
    def __init__(self, config_path='./config.ini'):
        if type(config_path) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
        elif type(self.config) == configparser.ConfigParser:
            self.config = config_path

    def submit(self, message):
        conversation = [{"role": "user", "content": message}]
        url = (self.config['CHATGPT']['BASICURL']) + \
              "/deployments/" + (self.config['CHATGPT']['MODELNAME']) + \
              "/chat/completions/?api-version=" + \
              (self.config['CHATGPT']['APIVERSION'])

        headers = {'Content-Type': 'application/json',
                   'api-key': (self.config['CHATGPT']['ACCESS_TOKEN'])}
        payload = {'messages': conversation}
        response = requests.post(url, json=payload, headers=headers)
        print('url: ', url)
        #         print('header: ',header)
        if response.status_code == 200:

            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return 'Error:', response


