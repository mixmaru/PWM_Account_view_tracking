# coding:utf-8
import logging
import sys
import traceback

from models import TrustsDataModel, ConfigModel

try:
    # ロガー設定
    logging.basicConfig(
        # level=getattr(logging, 'DEBUG'),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(module)s | %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        filename=ConfigModel.ConfigModel.LOGS_DIR + 'execute.log'
    )

    # 引数チェック
    if len(sys.argv) < 2:
        raise Exception("第一引数にブラウザを指定してくだしあ")

    # どのブラウザが指定されたか
    browser_name = sys.argv[1]
    if sys.argv[1] == "chrome":
        browser_type = TrustsDataModel.TrustsDataModel.BROWSER_CHROME
    elif sys.argv[1] == "phantomjs":
        browser_type = TrustsDataModel.TrustsDataModel.BROWSER_PHANTOMJS
    else:
        raise Exception("第一引数が正しくありません")

    logging.info('データ保存開始')
    trustsData = TrustsDataModel.TrustsDataModel(browser_type)
    trustsData.loadData()
    if not trustsData.alreadyWriteOutLog():
        trustsData.writeOutLog()
        logging.info('データ保存完了')
    logging.info('同日データがあるので保存しない')
except Exception:
    logging.error(traceback.format_exc())


