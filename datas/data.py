import pandas as pd
from . import utils


class DataStore:

    def __init__(self):
        super().__init__
        self.data_store = dict()
        self.grouped_data_store = dict()
        self.data_name_store = []


class BaseDataHandling:

    @staticmethod
    def csv_to_dataframe(file):
        return pd.read_csv(file, encoding='unicode-escape', low_memory=False)

    @staticmethod
    def drop_data(data, drop_items):
        loc_data = data.copy(deep=True)
        loc_data.drop(columns=drop_items, axis=1, inplace=True)
        loc_data.reset_index(drop=True, inplace=True)
        return loc_data

    @staticmethod
    def create_grouped_data_dict(data, key):
        group_dict = {}
        grouped = data.groupby(key)
        for name, group in grouped:
            group_dict[name] = group
            group_dict[name].reset_index(drop=True, inplace=True)
        return group_dict

    @staticmethod
    def drop_bad_data(data, value):
        loc_data = data.copy(deep=True)
        items_list =\
            utils.create_list_from_data_frame_columns(loc_data.columns)
        drop_item = []
        for item in items_list:
            if loc_data[item].isna().any():
                x = loc_data[item].isna().sum()
                y = len(loc_data[item])
                res = (x / y * 100)
                if res > value:
                    drop_item.append(item)
        loc_data.drop(columns=drop_item, axis=1, inplace=True)
        return loc_data
