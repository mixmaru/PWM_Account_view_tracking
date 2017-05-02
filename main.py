# coding:utf-8
from pprint import pprint
import ConfigParser

#初期化
#設定読み込み

import PwmSiteModel
site_model = PwmSiteModel.PwmSiteModel()
site_model.execute_load_data_from_web()

import InvestmentTrustsDataModel
trust_model = InvestmentTrustsDataModel.InvestmentTrustsDataModel()
trust_model.data1 = site_model.data1
trust_model.data2 = site_model.data2
trust_model.data3 = site_model.data3
trust_model.data4 = site_model.data4
trust_model.data5 = site_model.data5
trust_model.save_data()

