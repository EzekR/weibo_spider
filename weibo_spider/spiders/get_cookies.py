from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from hashlib import md5
import os

class GetCookie():
    accounts = [
        {
            'username': '13836889448',
            'password': 'Qq20190408'
        }
    ]

    def white_fuck(self):
        username = 'stefren'
        password = 'rl81789588'
        soft_id = '903605'
        password =  password.encode('utf8')
        cipher = md5(password).hexdigest()
        params = {
            'user': username,
            'pass2': cipher,
            'softid': soft_id,
            'codetype': 1902
        }
        headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }
        captcha = open(os.path.abspath('.')+'/spiders/image_cache/pin.png', 'rb').read()
        files = {
            'userfile': ('1.png', captcha)
        }
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=headers)
        json = eval(r.text)
        if json['err_no'] == 0:
            return json['pic_str']
        else:
            return 'error'

    def cache_pin(self, pin_url):
        r = requests.get(pin_url)
        with open(os.path.abspath('.')+'/spiders/image_cache/pin.png', 'wb') as f:
            f.write(r.content)
        captcha = self.white_fuck()
        return captcha
    
    def simulator(self):
        # browser settings
        options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values' :{
                'notifications' : 2
            }
        }
        options.add_experimental_option('prefs',prefs)
        driver = webdriver.Chrome(options = options)
        driver.set_window_size(1920, 1080)
        # open weibo and try login by account
        driver.get('https://weibo.com/')
        driver.implicitly_wait(10)
        driver.find_element_by_xpath(".//input[@node-type='username']").send_keys(self.accounts[0]['username'])
        time.sleep(1)
        driver.find_element_by_xpath(".//input[@node-type='password']").send_keys(self.accounts[0]['password'])
        time.sleep(1)
        # click login btn and wait for the captcha
        driver.find_element_by_xpath(".//a[@node-type='submitBtn']").click()
        time.sleep(5)
        pin_url = driver.find_element_by_xpath(".//img[@node-type='verifycode_image']").get_attribute('src')
        # if there is a captcha, there shall be a login try
        while pin_url!='about:blank':
            code = self.cache_pin(pin_url)
            # input captcha code
            driver.find_element_by_xpath(".//input[@node-type='verifycode']").send_keys(code)
            time.sleep(1)
            driver.find_element_by_xpath(".//a[@node-type='submitBtn']").click()
            time.sleep(5)
            # login success, return cookie
            if EC.title_contains(u"我的首页"):
                pin_url = 'about:blank'
                cookies = driver.get_cookies()
                return cookies
            else:
                pin_url = driver.find_element_by_xpath(".//img[@node-type='verifycode_image']").get_attribute('src')