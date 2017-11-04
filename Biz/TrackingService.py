from datetime import datetime
from selenium import webdriver
import selenium.common.exceptions
from . import Data
from . import Dao
import os


class TrackingService:
    BROWSER_CHROME = "chrome"
    BROWSER_PHANTOMJS = "phantomjs"
    __ENDPOINT_URL = 'https://webtools.pwm.co.jp/pwmservlet/pwm301.init'

    __CHROME_DRIVER_FILE = os.path.abspath("./chromedriver");
    __USER_EMAIL = None
    __PASSWORD = None
    __DATA_FILE_PATH = os.path.abspath("../data/data.csv");

    def __init__(self, user_email, password):
        self.__USER_EMAIL = user_email
        self.__PASSWORD = password

    def execute_tracking(self):
        try:
            self.__init_driver("chrome")
            data = Data.Data()
            """logging.info('ログイン開始')"""
            self.__login()
            """logging.info('ログイン完了')"""
            data.データ取得日時 = datetime.now()

            # 起点テーブル
            """logging.info('データ取得1開始')"""
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
            """logging.info('データ取得1完了')"""

            """logging.info('データ取得2開始')"""
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
            """logging.info('データ取得2完了')"""

            """データ保存"""
            dao = Dao.Dao(self.__DATA_FILE_PATH)
            dao.save_data(data)

        except selenium.common.exceptions.NoSuchElementException as e:
            self.__driver.save_screenshot('error.png')
            """logging.warning('データ取得に失敗があった')
            logging.warning(e.msg)"""
            # DOM出力
            """logging.warning(self.__driver.find_element_by_css_selector('body').get_attribute("innerHTML"))"""
        finally:
            self.__driver.quit()

    def __init_driver(self, browser_name: str):
        """logging.info('__initDriver開始')"""
        if browser_name == self.BROWSER_CHROME:
            self.__driver = webdriver.Chrome(self.__CHROME_DRIVER_FILE)
        elif browser_name == self.BROWSER_PHANTOMJS:
            self.__driver = webdriver.PhantomJS()
        else:
            raise Exception("不明なブラウザが指定されました")
        self.__driver.implicitly_wait(30)
        """logging.info('__initDriver完了')"""

    def __login(self):
        # phantomjsの場合パスワードの流し込みによくわからない挙動があり、頭に不要な1文字を追加して流し込む必要がある
        password = self.__PASSWORD
        if self.__driver.name == "phantomjs":
            password = "6" + password
        self.__driver.get(self.__ENDPOINT_URL)
        self.__driver.find_element_by_id('pwm30100-mail_address').send_keys(self.__USER_EMAIL)
        self.__driver.find_element_by_id('pwm30100-password').send_keys(password)
        self.__driver.find_element_by_id('pwm30100-btndef').click()


if __name__ == "__main__":
    import sys
    argv = sys.argv
    s = TrackingService(sys.argv[1], sys.argv[2])
    s.execute_tracking()
