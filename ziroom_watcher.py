import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import json
import random
import time
from requests_html import HTMLSession


class NotDoneError(Exception):
    pass


class NoConfigError(Exception):
    pass


class Watcher:
    def __init__(self, url):
        self.url = url
        self.session = HTMLSession()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        }
        self.get_info_url()

    def config(self, config):
        self.username = config['username']
        self.password = config['password']
        self.from_addr = config['username']
        self.to_addr = config['username']

    def get_info_url(self):
        house_info = self.session.get(self.url, headers=self.headers)
        room_id = house_info.html.find('#room_id')[0].attrs['value']
        house_id = house_info.html.find('#house_id')[0].attrs['value']
        self.info_url = 'http://www.ziroom.com/detail/info?id={}&house_id={}'.format(
            room_id, house_id)

    def sendmail(self, subject, text):
        message = MIMEText(text)
        message['From'] = Header("Ziroom_Watcher", 'utf-8')
        message['To'] = Header("Skywalker", 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')

        sm = smtplib.SMTP('smtp.qq.com', port=587)
        sm.ehlo()
        sm.starttls()
        sm.ehlo()
        sm.login(self.username, self.password)

        sm.sendmail(self.from_addr, self.to_addr, message.as_string())
        sm.quit()

    def get_final_info(self):
        response = self.session.get(
            self.info_url, headers=self.headers)
        info = json.loads(response.text)
        status = info['data']['status']
        if status != 'tzpzz':
            self.sendmail('房源状态已更新', '状态更新了')
        else:
            raise NotDoneError(status)

    def watch(self):
        try:
            self.username or not self.password
        except AttributeError:
            print('未正确配置邮件信息')
            return

        while True:
            try:
                self.get_final_info()
                break
            except NotDoneError as error:
                print(error)
                print(time.asctime(), '正在运行')
                time.sleep(random.randint(10, 25))

