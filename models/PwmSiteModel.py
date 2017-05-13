# coding:utf-8
from models import ConfigModel
from datetime import datetime
from selenium import webdriver


class PwmSiteModel:

    BROWSER_CHROME = "chrome"
    BROWSER_PHANTOMJS = "phantomjs"
    __ENDPOINT_URL = 'https://ifatools.pwm.co.jp/AccountView/Main/aw?awh=r&awssk=&dard=1#b0'
    __CHROME_DRIVER_FILE = ConfigModel.ConfigModel.ROOT_DIR + 'chromedriver'
    __USER_EMAIL = ConfigModel.ConfigModel.get_user_email()
    __PASSWORD = ConfigModel.ConfigModel.get_password()

    """Pwm日本証券のサイトにログインして、必要なデータを取得する"""
    def __init__(self, browser_name):
        if browser_name == self.BROWSER_CHROME:
            self.__driver = webdriver.Chrome(self.__CHROME_DRIVER_FILE)
        elif browser_name == self.BROWSER_PHANTOMJS:
            self.__driver = webdriver.PhantomJS()
        else:
            raise Exception("不明なブラウザが指定されました")

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
            driver.get(self.__ENDPOINT_URL)

            # ログイン
            driver.find_element_by_link_text('すでにログイン用のメールアドレスをお持ちの方はここをクリックしてログインしてください').click()
            driver.find_element_by_id('_bbni9').send_keys(self.__USER_EMAIL)
            driver.find_element_by_id('_g8y9pb').find_element_by_tag_name("input").send_keys(self.__PASSWORD)
            driver.find_element_by_id('_wltu3').find_element_by_css_selector('.rbBC.rbBFC.rbB').click()

            self.データ取得日時 = datetime.now()

            # 起点テーブル
            target_table_el = driver.find_element_by_xpath('//form[@action="/AccountView/Main/aw"]/div[1]/table/tbody')
            # お預かり合計、当日入金、金銭・MRF残高、残高合計（受渡基準）、残高合計（約低基準）取得
            基準日str = target_table_el.find_element_by_xpath('.//tr[1]/td/h3').text
            基準日str = 基準日str.replace('基準日: ', '')
            self.基準日 = datetime.strptime(基準日str, '%Y/%m/%d').date()
            self.お預かり合計 = int(target_table_el.find_element_by_xpath('.//tr[2]/td[4]').text.replace(',', ''))
            self.当日入金 = int(target_table_el.find_element_by_xpath('.//tr[3]/td[4]').text.replace(',', ''))
            self.金銭_MRF残高 = int(target_table_el.find_element_by_xpath('.//tr[4]/td[4]').text.replace(',', ''))
            self.残高合計_受渡基準 = int(target_table_el.find_element_by_xpath('.//tr[5]/td[4]').text.replace(',', ''))
            self.残高合計_約低基準 = int(target_table_el.find_element_by_xpath('.//tr[6]/td[4]').text.replace(',', ''))

            # ポートフォリオページ遷移
            driver.find_element_by_id('_rnvgk').click()

            # 世界債券（除日本）、国内大型株式、米国株式、新興国（分散型）株式、欧州株式、新興国債券、不動産投資信託（REAT）のパーセンテージ取得
            target_table_el = driver.find_element_by_xpath('//div[@class="tabPanel"][1]/table/tbody/tr[3]/td/div/table[1]/tbody/tr[2]/td[3]/div/table[2]/tbody')
            self.世界債券_除日本 = float(target_table_el.find_element_by_xpath('.//tr[1]/td[2]').text.replace('%', ''))
            self.国内大型株式 = float(target_table_el.find_element_by_xpath('.//tr[2]/td[2]').text.replace('%', ''))
            self.米国株式 = float(target_table_el.find_element_by_xpath('.//tr[3]/td[2]').text.replace('%', ''))
            self.新興国_分散型_株式 = float(target_table_el.find_element_by_xpath('.//tr[4]/td[2]').text.replace('%', ''))
            self.欧州株式 = float(target_table_el.find_element_by_xpath('.//tr[5]/td[2]').text.replace('%', ''))
            self.新興国債券 = float(target_table_el.find_element_by_xpath('.//tr[6]/td[2]').text.replace('%', ''))
            self.不動産投資信託_REAT = float(target_table_el.find_element_by_xpath('.//tr[7]/td[2]').text.replace('%', ''))

        finally:
            driver.quit()


