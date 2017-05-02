# coding:utf-8

class InvestmentTrustsDataModel:

    def __init__(self):
        self.データ取得日時 = None
        self.基準日 = None
        self.お預かり合計 = None
        self.当日入金 = None
        self.金銭_MRF残高 = None
        self.残高合計_受渡基準 = None
        self.残高合計_約低基準 = None

    def save(self):
        print("保存完了")
