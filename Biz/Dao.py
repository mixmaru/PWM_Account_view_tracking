import Biz.Data
import os
import csv


class Dao:
    def __init__(self, data_file_path: str):
        self.__DATA_FILE_PATH = data_file_path

    def save_data(self, data: Biz.Data.Data):
        """Dataの内容をcsvに保存する"""
        if os.path.exists(self.__DATA_FILE_PATH) is False:
            # csvファイルを作成する(header記入)
            self.__create_csv_file(self.__DATA_FILE_PATH)

        # データを追記
        with open(self.__DATA_FILE_PATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__get_data_list_for_csv(data))

    def __create_csv_file(self, csv_file_path: str):
        with open(csv_file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(self.__get_csv_header_list())

    @staticmethod
    def __get_csv_header_list():
        return ["データ取得日時", "基準日", "お預かり合計", "当日入金", "金銭_MRF残高", "残高合計_受渡基準", "残高合計_約低基準",
                "世界債券_除日本", "国内大型株式", "米国株式", "新興国_分散型_株式", "欧州株式", "新興国債券", "不動産投資信託_REAT"]

    @staticmethod
    def __get_data_list_for_csv(data:Biz.Data.Data):
        return [data.データ取得日時, data.基準日, data.お預かり合計, data.当日入金, data.金銭_MRF残高, data.残高合計_受渡基準, data.残高合計_約低基準,
                data.世界債券_除日本, data.国内大型株式, data.米国株式, data.新興国_分散型_株式, data.欧州株式, data.新興国債券, data.不動産投資信託_REAT]
