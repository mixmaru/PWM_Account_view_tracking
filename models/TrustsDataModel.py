from models import ConfigModel
from selenium import webdriver
import selenium.common.exceptions
from datetime import datetime
import os
import csv
import logging

class TrustsDataModel:

    BROWSER_CHROME = "chrome"
    BROWSER_PHANTOMJS = "phantomjs"
    __ENDPOINT_URL = 'https://webtools.pwm.co.jp/pwmservlet/pwm301.init'
    __CHROME_DRIVER_FILE = ConfigModel.ConfigModel.ROOT_DIR + 'chromedriver'
    __USER_EMAIL = ConfigModel.ConfigModel.get_user_email()
    __PASSWORD = ConfigModel.ConfigModel.get_password()
    __DATA_FILE_PATH = ConfigModel.ConfigModel.DATA_DIR + 'data.csv'

    def __init__(self, browser_name: str):
        self.__initDriver(browser_name)
        self.__initMember()

    def __initDriver(self, browser_name: str):
        logging.info('__initDriver開始')
        if browser_name == self.BROWSER_CHROME:
            self.__driver = webdriver.Chrome(self.__CHROME_DRIVER_FILE)
        elif browser_name == self.BROWSER_PHANTOMJS:
            self.__driver = webdriver.PhantomJS()
        else:
            raise Exception("不明なブラウザが指定されました")
        self.__driver.implicitly_wait(30)
        logging.info('__initDriver完了')

    def __initMember(self):
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

    def loadData(self):
        try:
            logging.info('ログイン開始')
            self.__login()
            logging.info('ログイン完了')
            self.データ取得日時 = datetime.now()

            # 起点テーブル
            logging.info('データ取得1開始')
            #target_table_el = self.__driver.find_element_by_xpath('//form[@action="/AccountView/Main/aw"]/div[1]/table/tbody')
            # お預かり合計、当日入金、金銭・MRF残高、残高合計（受渡基準）、残高合計（約低基準）取得
            基準日str = self.__driver.find_element_by_id('pwm30310-kijun_ymd').text
            self.基準日 = datetime.strptime(基準日str, '%Y/%m/%d').date()
            self.お預かり合計 = int(self.__driver.find_element_by_id('pwm30310-azukari_sum_uke').get_property("value").replace(',', ''))
            self.当日入金 = 0 #もうつかわれていない。csvフォーマットの為にのこしているだけ
            self.金銭_MRF残高 = int(self.__driver.find_element_by_id('pwm30310-kinsen_mrf_sum').get_property("value").replace(',', ''))
            self.残高合計_受渡基準 = int(self.__driver.find_element_by_id('pwm30310-zandaka_sum_uke').get_property("value").replace(',', ''))
            self.残高合計_約低基準 = int(self.__driver.find_element_by_id('pwm30310-zandaka_sum_yak').get_property("value").replace(',', ''))
            logging.info('データ取得1完了')

            logging.info('データ取得2開始')
            # ポートフォリオページ遷移
            self.__driver.find_element_by_id('pwm30310-btnportfolio').click()

            # 世界債券（除日本）、国内大型株式、米国株式、新興国（分散型）株式、欧州株式、新興国債券、不動産投資信託（REAT）のパーセンテージ取得
            self.世界債券_除日本 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-0').text.replace('%', ''))
            self.国内大型株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-1').text.replace('%', ''))
            self.米国株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-2').text.replace('%', ''))
            self.新興国_分散型_株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-3').text.replace('%', ''))
            self.欧州株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-4').text.replace('%', ''))
            self.新興国債券 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-5').text.replace('%', ''))
            self.不動産投資信託_REAT = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-6').text.replace('%', ''))
            logging.info('データ取得2完了')
        except selenium.common.exceptions.NoSuchElementException as e:
            self.__driver.save_screenshot('error.png')
            logging.warning('データ取得に失敗があった')
            logging.warning(e.msg)
            # DOM出力
            logging.warning(self.__driver.find_element_by_css_selector('body').get_attribute("innerHTML"))
        finally:
            self.__driver.quit()

    def writeOutLog(self):
        if os.path.exists(self.__DATA_FILE_PATH) is False:
            # csvファイルを作成する(header記入)
            self.__create_csv_file(self.__DATA_FILE_PATH)

        # データを追記
        with open(self.__DATA_FILE_PATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__get_data_list_for_csv())

    def alreadyWriteOutLog(self)->bool:
        # ログファイル自体存在しなければfalse
        if not os.path.exists(self.__DATA_FILE_PATH):
            return False
        else:
            with open(self.__DATA_FILE_PATH, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        csv基準日 = datetime.strptime(row[1], '%Y-%m-%d').date()
                    except ValueError as E:
                        #パースできない場合（ヘッダ行か、不明な形式でデータが入っていた場合）は無視して次の行へ
                        continue
                    if csv基準日 == self.基準日:
                        return True
                return False

    def __login(self):
        #phantomjsの場合パスワードの流し込みによくわからない挙動があり、頭に不要な1文字を追加して流し込む必要がある
        password = self.__PASSWORD
        if self.__driver.name == "phantomjs":
            password = "6" + password
        self.__driver.get(self.__ENDPOINT_URL)
        self.__driver.find_element_by_id('pwm30100-mail_address').send_keys(self.__USER_EMAIL)
        self.__driver.find_element_by_id('pwm30100-password').send_keys(password)
        self.__driver.find_element_by_id('pwm30100-btndef').click()

    def __create_csv_file(self, csv_file_path: str):
        with open(csv_file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__get_csv_header_list())


    @staticmethod
    def __get_csv_header_list():
        return ["データ取得日時", "基準日", "お預かり合計", "当日入金", "金銭_MRF残高", "残高合計_受渡基準", "残高合計_約低基準",
                "世界債券_除日本", "国内大型株式", "米国株式", "新興国_分散型_株式", "欧州株式", "新興国債券", "不動産投資信託_REAT"]

    def __get_data_list_for_csv(self):
        return [self.データ取得日時, self.基準日, self.お預かり合計, self.当日入金, self.金銭_MRF残高, self.残高合計_受渡基準, self.残高合計_約低基準,
                self.世界債券_除日本, self.国内大型株式, self.米国株式, self.新興国_分散型_株式, self.欧州株式, self.新興国債券, self.不動産投資信託_REAT]
