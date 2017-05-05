# coding:utf-8
import os
import csv
from models import ConfigModel


class InvestmentTrustsDataModel:

    __TARGET_CSV_FILE = ConfigModel.ConfigModel.DATA_DIR + 'data.csv'

    def __init__(self):
        self.データ取得日時 = None
        self.基準日 = None
        self.お預かり合計 = None
        self.当日入金 = None
        self.金銭_MRF残高 = None
        self.残高合計_受渡基準 = None
        self.残高合計_約低基準 = None

        self.世界債券_除日本 = None
        self.国内大型株式 = None
        self.米国株式 = None
        self.新興国_分散型_株式 = None
        self.欧州株式 = None
        self.新興国債券 = None
        self.不動産投資信託_REAT = None

    def save(self):
        csv_file = self.__TARGET_CSV_FILE
        if os.path.exists(csv_file) is False:
            # csvファイルを作成する(header記入)
            self.__create_csv_file()

        # データを追記
        with open(csv_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__get_data_list_for_csv())

    def __create_csv_file(self):
        with open(self.__TARGET_CSV_FILE, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__get_csv_header_list())

    @staticmethod
    def __get_csv_header_list():
        return ["データ取得日時", "基準日", "お預かり合計", "当日入金", "金銭_MRF残高", "残高合計_受渡基準", "残高合計_約低基準",
                "世界債券_除日本", "国内大型株式", "米国株式", "新興国_分散型_株式", "欧州株式", "新興国債券", "不動産投資信託_REAT"]

    @classmethod
    def __get_data_list_for_csv(cls):
        return [cls.データ取得日時, cls.基準日, cls.お預かり合計, cls.当日入金, cls.金銭_MRF残高, cls.残高合計_受渡基準, cls.残高合計_約低基準,
                cls.世界債券_除日本, cls.国内大型株式, cls.米国株式, cls.新興国_分散型_株式, cls.欧州株式, cls.新興国債券, cls.不動産投資信託_REAT]
