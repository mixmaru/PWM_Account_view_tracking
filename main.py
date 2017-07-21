# coding:utf-8
import logging
import sys
import traceback

from classes import PwmSite
from models import InvestmentTrustsDataModel, ConfigModel

try:
    # ロガー設定
    logging.basicConfig(
        # level=getattr(logging, 'DEBUG'),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(module)s | %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        filename=ConfigModel.ConfigModel.LOGS_DIR + 'execute.log'
    )
    _logger = logging.getLogger(__name__)

    # 引数チェック
    if len(sys.argv) < 2:
        raise Exception("第一引数にブラウザを指定してくだしあ")

    # どのブラウザが指定されたか
    browser_name = sys.argv[1]
    if sys.argv[1] == "chrome":
        browser_type = PwmSite.PwmSite.BROWSER_CHROME
    elif sys.argv[1] == "phantomjs":
        browser_type = PwmSite.PwmSite.BROWSER_PHANTOMJS
    else:
        raise Exception("第一引数が正しくありません")

    # Pwm証券からデータを取得
    _logger.info('データ取得開始')
    Pwm = PwmSite.PwmSite(browser_type)
    Pwm.execute_load_data()
    _logger.info('データ取得完了')

    # 取得したデータを保存
    _logger.info('データ保存開始')
    trust_model = InvestmentTrustsDataModel.InvestmentTrustsDataModel()
    trust_model.データ取得日時 = Pwm.データ取得日時
    trust_model.基準日 = Pwm.基準日
    trust_model.お預かり合計 = Pwm.お預かり合計
    trust_model.当日入金 = Pwm.当日入金
    trust_model.金銭_MRF残高 = Pwm.金銭_MRF残高
    trust_model.残高合計_約低基準 = Pwm.残高合計_約低基準
    trust_model.残高合計_受渡基準 = Pwm.残高合計_受渡基準
    trust_model.世界債券_除日本 = Pwm.世界債券_除日本
    trust_model.国内大型株式 = Pwm.国内大型株式
    trust_model.米国株式 = Pwm.米国株式
    trust_model.新興国_分散型_株式 = Pwm.新興国_分散型_株式
    trust_model.欧州株式 = Pwm.欧州株式
    trust_model.新興国債券 = Pwm.新興国債券
    trust_model.不動産投資信託_REAT = Pwm.不動産投資信託_REAT
    trust_model.save()
    _logger.info('データ保存完了')
except Exception:
    _logger.error(traceback.format_exc())


