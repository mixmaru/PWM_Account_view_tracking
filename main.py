# coding:utf-8
from models import PwmSiteModel, InvestmentTrustsDataModel
import logging
import traceback
import os

#ロガー設定
logging.basicConfig(
    #level=getattr(logging, 'DEBUG'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(module)s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    filename='./logs/execute.log'
)
_logger = logging.getLogger(__name__)

#ディレクトリパス
"""
#こんな風に定数を定義して使いたかったが、別ファイルからこの変数にアクセスできないので断念
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
DATA_DIT = ROOT_DIR + 'data/'
LOGS_DIR = ROOT_DIR + 'logs/'
MODELS_DIR = ROOT_DIR + 'models/'
"""

try:
    #Pwm証券からデータを取得
    _logger.info('データ取得開始')
    Pwm = PwmSiteModel.PwmSiteModel()
    Pwm.execute_load_data()
    _logger.info('データ取得完了')

    #取得したデータを保存
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


