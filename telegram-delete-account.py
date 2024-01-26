import requests
from bs4 import BeautifulSoup

class TelDeleteAccount(requests.Session):
    __password_url = 'https://my.telegram.org/auth/send_password'
    __login_url = 'https://my.telegram.org/auth/login'
    __do_delete = 'https://my.telegram.org/delete/do_delete'
    def __init__(self, number) -> None:
        super().__init__()
        self.phone_number = number
    def send_code(self):
        r = self.post(self.__password_url,data={'self.phone_number': self.phone_number})
        r = r.text
        return r['random_hash']
    def login(self):
        self.random_hash = self.send_code()
        password = input('Enter telegram password sent: ')
        data = {'self.phone_number': self.phone_number,
        'random_hash': self.random_hash,
        'password': password}
        r = self.post(self.__login_url,data=data)
        # print(r.text,r.json())
    def get_hash(self):
        r = self.get('https://my.telegram.org/delete')
        r = r.text
        b = BeautifulSoup(r,'html.parser')
        b:BeautifulSoup = b.find_all('script')[-1]
        b = b.text
        a = b.find('hash')+7
        c = 0
        h = ''
        while b[a+c] !="'":
            h = h+b[a+c]
            c+=1
        return h
    def delete(self):
        self.login()
        hash = self.get_hash(self.phone_number)
        r = self.post(self.__do_delete, data={'hash':hash})
        # print(self.random_hash)
        # return r 
        
        