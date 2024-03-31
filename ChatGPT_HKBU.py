import configparser
import requests


class HKBU_CHATGPT():
    def __init__(self, config_path='./config.ini'):
        if type(config_path) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
        elif type(self.config) == configparser.ConfigParser:
            self.config = config_path

    # def extract_name(self,message):
    #

    def submit(self, message):
        conversation = [{"role": "user", "content": "You are a professional chef, please help me determine whether the sentence contains the name of the dish in the following sentence. If so, only output the dish name. If not, only output 'no'. The sentence is: "+message}]
        url = (self.config['CHATGPT']['BASICURL']) + \
              "/deployments/" + (self.config['CHATGPT']['MODELNAME']) + \
              "/chat/completions/?api-version=" + \
              (self.config['CHATGPT']['APIVERSION'])

        headers = {'Content-Type': 'application/json',
                   'api-key': (self.config['CHATGPT']['ACCESS_TOKEN'])}
        payload = {'messages': conversation}
        response = requests.post(url, json=payload, headers=headers)
        # print(payload)
        #         print('header: ',header)
        if response.status_code == 200:

            data = response.json()
            # print(data)
            if data['choices'][0]['message']['content']!='no':

                return data['choices'][0]['message']['content'], 'yes'

            elif data['choices'][0]['message']['content']=='no':
                return 'Can not regonize the dish name, can you check again or deliver a more concrete description?','no'

        else:
            return 'Error:', response

    def submit2(self, dish_name):
        conversation = [{"role": "user", "content": "You are a professional chef and the dish name is "+dish_name+", please only output the following things 1.dish name 2. Required materials 3. Production Steps"}]
        url = (self.config['CHATGPT']['BASICURL']) + \
              "/deployments/" + (self.config['CHATGPT']['MODELNAME']) + \
              "/chat/completions/?api-version=" + \
              (self.config['CHATGPT']['APIVERSION'])

        headers = {'Content-Type': 'application/json',
                   'api-key': (self.config['CHATGPT']['ACCESS_TOKEN'])}
        payload = {'messages': conversation}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:

            data = response.json()
            # print(data)
            return data['choices'][0]['message']['content']




            # return data['choices'][0]['message']['content']
        else:
            return 'Error:', response


