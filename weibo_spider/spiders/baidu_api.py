import urllib
import requests
import base64
from hashlib import md5

def baidu_recog():
    try:
        temp_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=vRBSZAYqPGDMldHPMxR3uYSX&client_secret=zzhpPHuKUiOgtZvuj1vGjB3X252jvtUd'
        temp_res = requests.post(temp_url)
        print(temp_res.text)
        temp_token = eval(temp_res.text)['access_token']
        temp_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=' + temp_token
        temp_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        temp_file = open('../pin1.png', 'rb')
        temp_image = temp_file.read()
        temp_file.close()
        temp_data = {
            'image': base64.b64encode(temp_image)
        }
        temp_data = urllib.parse.urlencode(temp_data)
        temp_res = requests.post(url=temp_url, data=temp_data, headers=temp_headers)
        print(temp_res.text)
    except Exception as e:
        print(e)
        print('验证码识别异常，请联系管理员')

def white_fuck():
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
    captcha = open('image_cache/pin.png', 'rb').read()
    files = {
        'userfile': ('1.png', captcha)
    }
    r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=headers)
    json = eval(r.text)
    if json['err_no'] == 0:
        return json['pic_str']
    else:
        return 'error'


    
