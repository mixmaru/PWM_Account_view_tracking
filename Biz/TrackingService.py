import csv
import logging
from datetime import datetime
from selenium import webdriver
import selenium.common.exceptions
from Biz.Data import Data
from Biz.Dao import Dao
import os
from Biz.BrowserEnum import Browser


class TrackingService:
    BROWSER_CHROME = "chrome"
    BROWSER_PHANTOMJS = "phantomjs"

    __EXECUTE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

    __ENDPOINT_URL = 'https://webtools.pwm.co.jp/pwmservlet/pwm301.init'
    __CHROME_DRIVER_FILE = os.path.join(__EXECUTE_DIR_PATH, 'chromedriver')

    def execute_tracking(self, data_file_path: str, email: str, password: str) -> None:
        try:
            self.__init_driver(Browser.CHROME)
            data = Data()
            logging.info('ログイン開始')
            self.__login(email, password)
            logging.info('ログイン完了')
            data.データ取得日時 = datetime.now()

            # 起点テーブル
            logging.info('データ取得1開始')
            # target_table_el = self.__driver.find_element_by_xpath('//form[@action="/AccountView/Main/aw"]/div[1]/table/tbody')
            # お預かり合計、当日入金、金銭・MRF残高、残高合計（受渡基準）、残高合計（約低基準）取得
            基準日str = self.__driver.find_element_by_id('pwm30310-kijun_ymd').text
            data.基準日 = datetime.strptime(基準日str, '%Y/%m/%d').date()
            data.お預かり合計 = int(
                self.__driver.find_element_by_id('pwm30310-azukari_sum_uke').get_property("value").replace(',', ''))
            data.当日入金 = 0  # もうつかわれていない。csvフォーマットの為にのこしているだけ
            data.金銭_MRF残高 = int(
                self.__driver.find_element_by_id('pwm30310-kinsen_mrf_sum').get_property("value").replace(',', ''))
            data.残高合計_受渡基準 = int(
                self.__driver.find_element_by_id('pwm30310-zandaka_sum_uke').get_property("value").replace(',', ''))
            data.残高合計_約低基準 = int(
                self.__driver.find_element_by_id('pwm30310-zandaka_sum_yak').get_property("value").replace(',', ''))
            logging.info('データ取得1完了')

            logging.info('データ取得2開始')
            # ポートフォリオページ遷移
            self.__driver.find_element_by_id('pwm30310-btnportfolio').click()

            # 世界債券（除日本）、国内大型株式、米国株式、新興国（分散型）株式、欧州株式、新興国債券、不動産投資信託（REAT）のパーセンテージ取得
            data.世界債券_除日本 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-0').text.replace('%', ''))
            data.国内大型株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-1').text.replace('%', ''))
            data.米国株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-2').text.replace('%', ''))
            data.新興国_分散型_株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-3').text.replace('%', ''))
            data.欧州株式 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-4').text.replace('%', ''))
            data.新興国債券 = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-5').text.replace('%', ''))
            data.不動産投資信託_REAT = float(self.__driver.find_element_by_id('pwm10731-m7_hiritu-6').text.replace('%', ''))
            logging.info('データ取得2完了')

            # データ保存
            if self.__alreadyWriteOutLog(data.基準日, data_file_path):
                # すでに同日データが存在するので保存しない
                logging.info('同日データがあるので保存しない')
            else:
                # 同日データは存在しないので、保存する
                dao = Dao(data_file_path)
                dao.save_data(data)
                logging.info('データ保存完了')

        except selenium.common.exceptions.NoSuchElementException as e:
            self.__driver.save_screenshot('error.png')
            logging.warning('データ取得に失敗があった')
            logging.warning(e.msg)
            # DOM出力
            logging.warning(self.__driver.find_element_by_css_selector('body').get_attribute("innerHTML"))
        finally:
            self.__driver.quit()

    def __init_driver(self, browser: Browser) -> None:
        logging.info('__initDriver開始')
        if browser == Browser.CHROME:
            self.__driver = webdriver.Chrome(self.__CHROME_DRIVER_FILE)
        elif browser == Browser.PHANTOMJS:
            self.__driver = webdriver.PhantomJS()
        else:
            raise Exception("不明なブラウザが指定されました")
        self.__driver.implicitly_wait(30)
        logging.info('__initDriver完了')

    def __login(self, email: str, password: str) -> None:
        # phantomjsの場合パスワードの流し込みによくわからない挙動があり、頭に不要な1文字を追加して流し込む必要がある
        password = password
        if self.__driver.name == "phantomjs":
            password = "6" + password
        self.__driver.get(self.__ENDPOINT_URL)
        self.__driver.find_element_by_id('pwm30100-mail_address').send_keys(email)
        self.__driver.find_element_by_id('pwm30100-password').send_keys(password)
        self.__driver.find_element_by_id('pwm30100-btndef').click()

    def __alreadyWriteOutLog(self, 基準日: datetime, data_file_path: str) -> bool:
        # ログファイル自体存在しなければfalse
        if not os.path.exists(data_file_path):
            return False
        else:
            with open(data_file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        csv基準日 = datetime.strptime(row[1], '%Y-%m-%d').date()
                    except ValueError as E:
                        # パースできない場合（ヘッダ行か、不明な形式でデータが入っていた場合）は無視して次の行へ
                        continue
                    if csv基準日 == 基準日:
                        return True
                return False
