# coding:utf-8
from models import PwmSiteModel, InvestmentTrustsDataModel

#Pwm証券からデータを取得
site_model = PwmSiteModel.PwmSiteModel()
site_model.execute_load_data()

#取得したデータを保存
trust_model = InvestmentTrustsDataModel.InvestmentTrustsDataModel()
trust_model.データ取得日時 = site_model.データ取得日時
trust_model.基準日 = site_model.基準日
trust_model.お預かり合計 = site_model.お預かり合計
trust_model.当日入金 = site_model.当日入金
trust_model.金銭_MRF残高 = site_model.金銭_MRF残高
trust_model.残高合計_約低基準 = site_model.残高合計_約低基準
trust_model.残高合計_受渡基準 = site_model.残高合計_受渡基準
trust_model.save()

