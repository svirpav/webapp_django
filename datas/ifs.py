from . import utils
import pandas as pd


class Ifs_Base:

    def __init__(self):
        super().__init__

    @staticmethod
    def csv_to_dataframe(file):
        return pd.read_csv(file, encoding='unicode-escape', low_memory=False)

    ''' Data Cleaing '''

    @staticmethod
    def clean_data(data, sellected_items):
        cln_data = pd.DataFrame()
        for item in sellected_items:
            tmp = []
            tmp = data[item]
            cln_data[item] = pd.Series(tmp)
        return cln_data

    @staticmethod
    def return_grouped_data_dict(data, key):
        group_dict = {}
        grouped = data.groupby(key)
        for name, group in grouped:
            group_dict[name] = group
            group_dict[name].reset_index(drop=True, inplace=True)
        return group_dict

    @staticmethod
    def remove_bad_data(data, value, items_list):
        loc_data = data.copy()
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

    ''' Formating Data '''

    @staticmethod
    def object_to_string(data, item_list):
        loc_data = data.copy()
        for item in item_list:
            try:
                loc_data[item] = loc_data[item].astype('string')
            except ValueError as err:
                print(err, ':', item)
        return loc_data

    @staticmethod
    def convert_to_categorical(data, item_list):
        loc_data = data.copy()
        for item in item_list:
            loc_data[item] = loc_data[item].astype('category')
        return loc_data

    @staticmethod
    def convert_to_datetime(data, item_list):
        loc_data = data.copy()
        error_list = []
        for item in item_list:
            try:
                loc_data[item] = loc_data[item].astype('object')
                loc_data[item] = loc_data[item].astype('datetime64')
            except ValueError as err:
                print(format(err), ':', item)
                error_list.append(item)
        for error in error_list:
            utils.datetime_error_handling(loc_data[error])
        return loc_data

    ''' Helping Functions '''

    @staticmethod
    def return_df_cols_list(df_columns):
        columns = []
        for item in df_columns:
            columns.append(item)
        return columns

    @staticmethod
    def create_group_columns(nr_of_cols, item_list):
        length = len(item_list)
        cell_size = utils.get_cell_size(length, nr_of_cols)
        start = 0
        end = cell_size
        grp_columns = []
        for i in range(nr_of_cols):
            grp_columns.append(item_list[start:end])
            start = end
            end = end + cell_size
            if end > length:
                end = length
        return grp_columns

    @staticmethod
    def find_and_return_date_items(item_list, key, data_column_list):
        i_lst = item_list.copy()
        cl_lst = data_column_list.copy()
        for item in cl_lst:
            if key in item:
                i_lst.append(item)
        return i_lst

    @staticmethod
    def return_app_list():
        return ['Customer',
                'Sales Part',
                'Site']

    ''' Under modification '''

    def __clean_data(self, sellected_items):
        cln_data = pd.DataFrame()
        for item in sellected_items:
            data = []
            data = self._raw_df[item]
            cln_data[item] = pd.Series(data)
        return cln_data

    def __sellect_data_to_erase(self):
        available_data = []
        if self._raw_df is not None:
            available_data.append('raw')
        if self._cln_data is not None:
            available_data.append('cleaned')
        return available_data

    def __erase_sellected_data(self, items):
        if 'raw' in items:
            self._raw_df = None
        if 'cleaned' in items:
            self._cln_data = None