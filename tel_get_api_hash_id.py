import requests
from bs4 import BeautifulSoup






class GetApiIdApiHash:
    __send_password_url = 'https://my.telegram.org/auth/send_password'
    __login_url = 'https://my.telegram.org/auth/login'
    __create_api_url = 'https://my.telegram.org/apps/create'
    __app_url = 'https://my.telegram.org/apps'
    __request = requests.Session()
    __request.headers.update({'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 TelegramBot (like TwitterBot)'})
    def __init__(self, number):
        # self.login_try = 0 
        self.__number = number
        r = self.__request.post(self.__send_password_url, data={'phone': self.__number})
        self.__random_hash = r.json()['random_hash']
        self.__password = input('Enter recived password: ')
        
    def __login(self):
        data = {
            'phone': self.__number,
            'random_hash': self.__random_hash,
            'password': self.__password
        }
        login = self.__request.post(self.__login_url, data=data).text
        # print(login)
        # self.login_try += 1
        if login == 'Invalid confirmation code!':
            self.__password = input('Invalid confirmation code!\nEnter recived password: ')
            # print(self.login_try)
            self.__login()
        elif login == 'Sorry, too many tries. Please try again later.':
            return False
        else:
            return self
    
    def get_api_id_hash(self):
        self.__login()
        r = self.__request.get(self.__app_url)
        bs4 = BeautifulSoup(r.text, 'html.parser')
        hash = bs4.find('input',{'name':'hash'})['value']
        
        data = {
            'hash': hash,
            'app_title': 'pythonbot',
            'app_shortname': 'python',
            '__': '',
            'app_platform' : 'desktop',
            'app_desc': '',
        }
        r = self.__request.post(self.__create_api_url, data=data)
        if r.text == 'ERROR':
            # print('error')
            self.get_api_id_hash() 
        elif r.text == '':
            # print('ok')
            self.get_api_id_hash() 
        else:
            bs4 = BeautifulSoup(r.text, 'html.parser')
            api_id = bs4.find_all('strong')[0].text
            api_hash = bs4.find_all('span')[2].text
            return {'api_id':api_id, 'api_hash':api_hash}