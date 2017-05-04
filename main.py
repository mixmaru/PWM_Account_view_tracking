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
trust_model.世界債券_除日本 = site_model.世界債券_除日本
trust_model.国内大型株式 = site_model.国内大型株式
trust_model.米国株式 = site_model.米国株式
trust_model.新興国_分散型_株式 = site_model.新興国_分散型_株式
trust_model.欧州株式 = site_model.欧州株式
trust_model.新興国債券 = site_model.新興国債券
trust_model.不動産投資信託_REAT = site_model.不動産投資信託_REAT
trust_model.save()

