from . import utils
from . import ifs
from . import data
from datetime import datetime


class App:

    __context = {}

    def __init__(self, name):
        self.__context['app'] = name

    def main(self, request):
        if request.method == 'POST':
            response = utils.query_dict_to_dict(request.POST)
            if self.__app_chng_rqst(response):
                self.__dlt_app_data()
                self.__set_app(response['app-btn'])
            else:
                if self.__context['app'] == 'base':
                    pass
                elif self.__context['app'] == 'ifs':
                    if 'ifs-btn' in response:
                        self.__context = self.ifs.handler(request)
        elif request.method == 'GET':
            print('GET')
        else:
            print('WTF')
        return self.__context

    def __app_chng_rqst(self, response):
        if 'app-btn' in response:
            if response['app-btn'] != self.__context['app']:
                return True
            else:
                return False
        else:
            return False

    def __set_app(self, name):
        self.__context['app'] = name
        if name == 'ifs':
            self.__context['ifs'] = 'base'
            self.ifs = Ifs(self.__context)

    def __dlt_app_data(self):
        # self.__context = None
        self.__context['app'] = 'base'


class Ifs:

    __context = {}

    def __init__(self, context):
        super().__init__()
        self.__context = context
        self.__ifs_base = ifs.Ifs_Base()
        self.__data = data.IFS()
        self.__items = utils.Categories()

    def handler(self, request):
        response = utils.query_dict_to_dict(request.POST)
        if self.__context['ifs'] == 'base':
            if response['ifs-btn'] == 'load':
                self.__context['ifs_view'] = 'load'
            elif response['ifs-btn'] == 'upload':
                try:
                    idx = utils.create_file_name(
                        datetime.now().strftime('%Y-%m-%d %H:%M'), '_',
                        request.FILES['data'].name)
                    self.__data.data_name_store.append(idx)
                    self.__data.data_store[idx] =\
                        self.__ifs_base.csv_to_dataframe(request.FILES['data'])
                    self.__context['file_sellections'] =\
                        self.__data.data_name_store
                    self.__context['ifs_view'] = 'file_sellection'
                    self.__context['ifs_files'] = True
                except KeyError as error:
                    print(format(error), 'file was not loaded')
            elif response['ifs-btn'] == 'prepare':
                data = self.__data.data_store[response['file_sellected']]
                # print('IN :', data.memory_usage(deep=True).sum())
                data =\
                    self.__ifs_base.clean_data(
                        data, self.__items.presellected_items)
                column_list = self.__ifs_base.return_df_cols_list(data)
                data = self.__ifs_base.object_to_string(data, column_list)
                # print('FM :', data.memory_usage(deep=True).sum())
                self.__data.data_store[response['file_sellected']] = data
                grouped_data =\
                    self.__ifs_base.return_grouped_data_dict(
                        data, 'Order Type')
                for item in grouped_data:
                    grouped_data[item] =\
                        self.__ifs_base.remove_bad_data(
                            grouped_data[item], 95, column_list)
                    grp_column_lst =\
                        self.__ifs_base.return_df_cols_list(grouped_data[item])
                    ctegorical_items = self.__items.categorical_items
                    for unit in ctegorical_items:
                        if unit not in grp_column_lst:
                            ctegorical_items.remove(unit)
                    grouped_data[item] =\
                        self.__ifs_base.convert_to_categorical(
                            grouped_data[item], ctegorical_items)
                    datetime_item =\
                        self.__ifs_base.find_and_return_date_items(
                            self.__items.datetime_items,
                            'Date', grp_column_lst)
                    grouped_data[item] =\
                        self.__ifs_base.convert_to_datetime(
                            grouped_data[item], datetime_item)
                # print(self.__data.data_store[response['file_sellected']])
            elif response['ifs-btn'] == 'files':
                self.__context['ifs_view'] = 'file_sellection'
            elif response['ifs-btn'] == 'process':
                try:
                    self.__data =\
                        self.__ifs_base.csv_to_dataframe(request.FILES['data'])
                    cols_list =\
                        self.__ifs_base.return_df_cols_list(
                            self.__data.columns)
                    grp_data_dict =\
                        self.__ifs_base.return_grouped_data_dict(
                            self.__data, 'Order Type')
                    view_data = dict()
                    for name in grp_data_dict:
                        grp_data_dict[name] =\
                            self.__ifs_base.remove_bad_data(
                                grp_data_dict[name], 80, cols_list)
                        view_data[name] =\
                            self.__ifs_base.return_df_cols_list(
                                grp_data_dict[name].columns)
                    for name in view_data:
                        view_data[name] =\
                            self.__ifs_base.create_group_columns(
                                4, view_data[name])
                    self.__context['ifs_view'] = 'data_sellection'
                    self.__context['ifs__view_data'] = view_data
                except KeyError:
                    pass
            elif response['ifs-btn'] == 'clean-data':
                print(response)
        elif self.__context['ifs'] == 'customer':
            pass
        return self.__context
