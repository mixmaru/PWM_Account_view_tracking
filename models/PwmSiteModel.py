# coding:utf-8
import configparser
from datetime import datetime
from selenium import webdriver

class PwmSiteModel:
    """Pwm日本証券のサイトにログインして、必要なデータを取得する"""
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.__url = config.get('common', 'endpoint_url')
        self.__driver = webdriver.Chrome(executable_path=config.get('require', 'chrome_driver_path'))
        self.__user_email = config.get('secure', 'user_email')
        self.__password = config.get('secure', 'password')

        self.データ取得日時 = None
        self.基準日 = None
        self.お預かり合計 = None
        self.当日入金 = None
        self.金銭_MRF残高 = None
        self.残高合計_受渡基準 = None
        self.残高合計_約低基準 = None

        self.世界債券_除日本 = None
        self.国内大型株式 = None
        self.米国株式 = None
        self.新興国_分散型_株式 = None
        self.欧州株式 = None
        self.新興国債券 = None
        self.不動産投資信託_REAT = None

    def execute_load_data(self):
        try:
            driver = self.__driver
            driver.implicitly_wait(30)
            driver.get(self.__url)

            #ログイン
            driver.find_element_by_link_text('すでにログイン用のメールアドレスをお持ちの方はここをクリックしてログインしてください').click()
            driver.find_element_by_id('_bbni9').send_keys(self.__user_email)
            driver.find_element_by_id('_g8y9pb').find_element_by_tag_name("input").send_keys(self.__password)
            driver.find_element_by_id('_wltu3').find_element_by_css_selector('.rbBC.rbBFC.rbB').click()

            self.データ取得日時 = datetime.now()

            #お預かり合計、当日入金、金銭・MRF残高、残高合計（受渡基準）、残高合計（約低基準）取得
            基準日str = driver.find_element_by_xpath('//*[@id="_lkhqec"]/table/tbody/tr[1]/td').text
            基準日str = 基準日str.replace('基準日: ', '')
            self.基準日 = datetime.strptime(基準日str, '%Y/%m/%d').date()
            self.お預かり合計 = int(driver.find_element_by_xpath('//*[@id="_lkhqec"]/table/tbody/tr[2]/td[4]').text.replace(',', ''))
            self.当日入金 = int(driver.find_element_by_xpath('//*[@id="_lkhqec"]/table/tbody/tr[3]/td[4]').text.replace(',', ''))
            self.金銭_MRF残高 = int(driver.find_element_by_xpath('//*[@id="_lkhqec"]/table/tbody/tr[4]/td[4]').text.replace(',', ''))
            self.残高合計_受渡基準 = int(driver.find_element_by_xpath('//*[@id="_lkhqec"]/table/tbody/tr[5]/td[4]').text.replace(',', ''))
            self.残高合計_約低基準 = int(driver.find_element_by_xpath('//*[@id="_lkhqec"]/table/tbody/tr[6]/td[4]').text.replace(',', ''))

            #ポートフォリオページ遷移
            driver.find_element_by_id('_rnvgk').click()

            #世界債券（除日本）、国内大型株式、米国株式、新興国（分散型）株式、欧州株式、新興国債券、不動産投資信託（REAT）のパーセンテージ取得
            self.世界債券_除日本 = float(driver.find_element_by_xpath('//*[@id="_azzo4d"]/table[2]/tbody/tr[1]/td[2]').text.replace('%', ''))
            self.国内大型株式 = float(driver.find_element_by_xpath('//*[@id="_azzo4d"]/table[2]/tbody/tr[2]/td[2]').text.replace('%', ''))
            self.米国株式 = float(driver.find_element_by_xpath('//*[@id="_azzo4d"]/table[2]/tbody/tr[3]/td[2]').text.replace('%', ''))
            self.新興国_分散型_株式 = float(driver.find_element_by_xpath('//*[@id="_azzo4d"]/table[2]/tbody/tr[4]/td[2]').text.replace('%', ''))
            self.欧州株式 = float(driver.find_element_by_xpath('//*[@id="_azzo4d"]/table[2]/tbody/tr[5]/td[2]').text.replace('%', ''))
            self.新興国債券 = float(driver.find_element_by_xpath('//*[@id="_azzo4d"]/table[2]/tbody/tr[6]/td[2]').text.replace('%', ''))
            self.不動産投資信託_REAT = float(driver.find_element_by_xpath('//*[@id="_azzo4d"]/table[2]/tbody/tr[7]/td[2]').text.replace('%', ''))

        finally:
            driver.quit()


