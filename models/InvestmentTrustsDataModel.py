# coding:utf-8
import os
import csv

class InvestmentTrustsDataModel:

    def __init__(self):
        self.__target_csv = './data/data.csv'

        self.データ取得日時 = None
        self.基準日 = None
        self.お預かり合計 = None
        self.当日入金 = None
        self.金銭_MRF残高 = None
        self.残高合計_受渡基準 = None
        self.残高合計_約低基準 = None

    def save(self):
        csv_file = self.__target_csv
        if os.path.exists(csv_file) == False:
            #csvファイルを作成する(header記入)
            self.__createCsvFile()

        #データを追記
        with open(csv_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__getDataListForCsv())

    def __createCsvFile(self):
        with open(self.__target_csv, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__getCsvHeaderList())

    def __getCsvHeaderList(self):
        return ["データ取得日時", "基準日", "お預かり合計", "当日入金", "金銭_MRF残高", "残高合計_受渡基準", "残高合計_約低基準"]

    def __getDataListForCsv(self):
        ret_list = [self.データ取得日時, self.基準日, self.お預かり合計, self.当日入金, self.金銭_MRF残高, self.残高合計_受渡基準, self.残高合計_約低基準]
        return ret_list
