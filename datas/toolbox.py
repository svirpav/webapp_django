import pandas as pd


class Toolbox:

    def __init__(self):
        self.raw_data_frame = None
        self.raw_data_frame_columns = []
        self.sellected_items = []
        self.app_list = []
        self.customer_list = []

    ''' From here you can retrive data stored in application '''

    def get_data(self):
        return self.raw_data_frame

    def get_sellected_list(self):
        return self.sellected_items

    def get_app_list(self):
        return self.app_list

    def get_raw_df_columns(self):
        return self.raw_data_frame_columns

    def get_customer_list(self):
        return self.customer_list

    ''' Here is data operations functions '''

    def create_raw_df(self, file):
        self.raw_data_frame = pd.read_csv(file, encoding='unicode-escape',
                                          dtype='object')

    def create_raw_df_columns(self):
        for i in self.raw_data_frame.columns:
            self.raw_data_frame_columns.append(i)

    def save_sellected_columns(self, sellected):
        self.sellected_items = sellected

    def q_dict_handler(self, q_dict):
        q = q_dict
        if q.__contains__('ctx'):
            a = q.getlist('ctx')
        else:
            a = None
        return a

    def query_dict_to_list(self, q_dict):
        q = q_dict
        if q.__contains__('ctx'):
            q_list = q.getlist('ctx')
            if len(q_list) != 0:
                return q_list
            else:
                return None
        else:
            return None

    def query_dictionary_handler(self, q_dict, keys):
        res_dict = {}
        for key in keys:
            if q_dict.__contains__(key):
                res_dict[key] = q_dict.getlist(key)
        return res_dict

    def create_app_list(self, selected_items):
        self.app_list = []
        if 'Customer No' in selected_items:
            self.app_list.append('Customer Analysis')
        if 'Sales Part No' in selected_items:
            self.app_list.append('Sales Part Analysis')
        if 'Site' in selected_items:
            self.app_list.append('Site Analysis')

    def create_customer_list(self):
        for i in self.raw_data_frame['Customer No']:
            if i not in self.customer_list:
                self.customer_list.append(i)
        self.customer_list = sorted(self.customer_list)

    def return_cleaned_data(self, raw_data, sellected):
        clean_data = pd.DataFrame()
        for column in sellected:
            col = []
            col = raw_data[column]
            clean_data[column] = pd.Series(col)
        return clean_data

    def create_and_return_group(self, data, grp_name):
        grp_data = data.groupby('Customer No')
        grp_data = grp_data.get_group(grp_name)
        grp_data.reset_index(drop=True, inplace=True)
        return grp_data

    def clear_data(self):
        self.raw_data_frame = None
        self.raw_data_frame_columns = []
        self.sellected_items = []
        self.app_list = []
        self.customer_list = []
