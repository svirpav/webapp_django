from . import utils
from . import ifs
from . import data


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
                    self.__context = self.ifs.app(request)
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
            self.ifs = IfsApp(self.__context)

    def __dlt_app_data(self):
        self.__context = dict()
        self.__context['app'] = 'base'


class IfsApp:

    __context = {}

    def __init__(self, context):
        super().__init__()
        self.__context = context
        self.__prepare = ifs.PepareData()
        self.__data = data.DataStore()
        self.__categories = ifs.DataCategories()

    def app(self, request):
        response = utils.query_dict_to_dict(request.POST)
        if self.__context['ifs'] == 'base':
            if response['ifs-btn'] == 'load':
                self.__context['ifs_view'] = 'load'
            elif response['ifs-btn'] == 'upload':
                try:
                    file = request.FILES['data']
                    self.__load_and_store(file)
                except KeyError as error:
                    print(format(error), 'file was not loaded')
            elif response['ifs-btn'] == 'prepare':
                try:
                    data_location = response['file_sellected']
                    self.__format_data(data_location)
                    view_data = dict()
                    grp_data = self.__data.grouped_data_store[data_location]
                    for name in grp_data:
                        view_data[name] =\
                            utils.create_list_from_data_frame_columns(
                                grp_data[name])
                    for name in view_data:
                        view_data[name] =\
                            utils.create_grouped_list(
                                4, view_data[name])
                    self.__context['ifs_view'] = 'data_sellection'
                    self.__context['ifs__view_data'] = view_data
                except KeyError as err:
                    print(format(err))
                    self.__context['ifs_view'] = 'base'
                # print(self.__data.data_store[response['file_sellected']])
            elif response['ifs-btn'] == 'files':
                self.__context['ifs_view'] = 'file_sellection'
            elif response['ifs-btn'] == 'sellect':
                self.__context['available_apps'] =\
                    self.__create_app_list_dict(response)
                self.__context['ifs_view'] = 'sub_app_sellection'
            elif response['ifs-btn'] == 'INT_Customer'\
                    or 'NO_Customer'\
                    or 'SEO_Customer'\
                    or 'WAR_Customer':
                self.__context['ifs'] = 'customer'
            elif response['ifs-btn'] == 'INT_SalesPart'\
                    or 'NO_SalesPart'\
                    or 'SEO_SalesPart'\
                    or 'WAR_SalesPart':
                self.__context['ifs'] = 'salespart'
            elif response['ifs-btn'] == 'INT_Site'\
                    or 'NO_Site'\
                    or 'SEO_Site'\
                    or 'WAR_Site':
                self.__context['ifs'] = 'site'
            elif response['ifs-btn'] == 'clean-data':
                print(response)
            else:
                print(response)
        elif self.__context['ifs'] == 'customer':
            pass
        return self.__context

    def __load_and_store(self, file):
        idx = utils.create_data_dispay_name(file.name)
        self.__data.data_name_store.append(idx)
        self.__data.data_store[idx] =\
            self.__prepare.csv_to_dataframe(file)
        self.__context['file_sellections'] =\
            self.__data.data_name_store
        self.__context['ifs_view'] = 'file_sellection'
        self.__context['ifs_files'] = True

    def __format_data(self, data_location):
        data = self.__data.data_store[data_location].copy(deep=True)
        # print('IN :', data.memory_usage(deep=True).sum())
        drop_items =\
            utils.remove_set_from_list(
                utils.create_list_from_data_frame_columns(data.columns),
                self.__categories.presellected_items)
        data = self.__prepare.drop_data(data, drop_items)
        exempt_list = list(set(self.__categories.categorical_items +
                               self.__categories.datetime_items +
                               self.__categories.integer_items +
                               self.__categories.float_items))
        data =\
            self.__prepare._to_string(data, exempt_list)
        self.__data.data_store[data_location] = data.copy(deep=True)
        grouped_data =\
            self.__prepare.create_grouped_data_dict(
                data, 'Order Type')
        for item in grouped_data:
            print('Handling group : ', item)
            grouped_data[item] =\
                self.__prepare.drop_bad_data(grouped_data[item], 95)
            grouped_data[item] =\
                self.__prepare._to_categorical(
                    grouped_data[item],
                    self.__categories.categorical_items)
            grouped_data[item] =\
                self.__prepare._to_datetime(
                    grouped_data[item], self.__categories.datetime_items)
            grouped_data[item] =\
                self.__prepare._to_int(
                    grouped_data[item], self.__categories.integer_items)
            grouped_data[item] =\
                self.__prepare._to_float(
                    grouped_data[item], self.__categories.float_items)
            for name in self.__categories.date_series:
                grouped_data[item][name] =\
                    self.__prepare._create_date_series(
                    grouped_data[item]['Created'], name)
        self.__data.grouped_data_store[data_location] =\
            grouped_data.copy()

    def __create_app_list_dict(self, response):
        app_list_dict = dict()
        if 'order_type' in response:
            if isinstance(response['order_type'], list):
                for item in response['order_type']:
                    app_list_dict[item] =\
                        self.__create_app_list(response[item])
            else:
                app_list_dict[response['order_type']] =\
                    self.__create_app_list(response[response['order_type']])
        return app_list_dict

    def __create_app_list(self, items_list):
        app_list = []
        if set(self.__categories.customer_app_preset).issubset(items_list):
            app_list.append('Customer')
        if set(self.__categories.salespart_app_preset).issubset(items_list):
            app_list.append('SalesPart')
        if set(self.__categories.site_app_preset).issubset(items_list):
            app_list.append('Site')
        return app_list
