# coding:utf-8
from models import PwmSiteModel, InvestmentTrustsDataModel

#Pwm証券からデータを取得
site_model = PwmSiteModel.PwmSiteModel()
site_model.execute_load_data_from_web()

#取得したデータを保存
trust_model = InvestmentTrustsDataModel.InvestmentTrustsDataModel()
trust_model.data1 = site_model.data1
trust_model.data2 = site_model.data2
trust_model.data3 = site_model.data3
trust_model.data4 = site_model.data4
trust_model.data5 = site_model.data5
trust_model.save_data()

