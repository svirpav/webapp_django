import pandas as pd


class DataHandler:

    def __init__(self):
        self.raw_data_frame = None
        self.raw_data_frame_columns = []
        self.sellected_items = []
        self.app_list = []

    ''' From here you can retrive data stored in application '''

    def get_data(self):
        return self.raw_data_frame

    def get_sellected_list(self):
        return self.sellected_items

    def get_app_list(self):
        return self.app_list

    def get_raw_df_columns(self):
        return self.raw_data_frame_columns

    ''' Here is data operations functions '''

    def save_file_as_df(self, file):
        self.raw_data_frame = pd.read_csv(file, encoding='unicode-escape',
                                          dtype='object')

    def return_df_col_names(self):
        for i in self.raw_data_frame.columns:
            self.raw_data_frame_columns.append(i)
        return self.raw_data_frame_columns

    def save_sellected_columns(self, sellected):
        self.sellected_items = sellected

    def q_dict_handler(self, q_dict):
        q = q_dict
        if q.__contains__('ctx'):
            a = q.getlist('ctx')
        else:
            a = None
        return a

    def create_app_list(self, selected_items):
        if 'Customer No' in selected_items:
            self.app_list.append('Customer Analysis')
        if 'Sales Part No' in selected_items:
            self.app_list.append('Sales Part Analysis')
        if 'Site' in selected_items:
            self.app_list.append('Site Analysis')
        return self.app_list
