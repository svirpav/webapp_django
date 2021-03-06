''' UTILS '''
from datetime import datetime
import dateutil
import pandas as pd
import locale
import math


def query_dict_to_dict(qdict):
    q_dict = {}
    a = qdict.dict()
    for item in a:
        q_dict[item] = qdict.getlist(item)
    q_dict = __dict_handler(q_dict)
    return q_dict


def __dict_handler(ddict):
    response = ddict
    for item in response:
        if len(response[item]) == 1:
            response[item] = response[item][0]
    return response


def create_data_dispay_name(file_name):
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    sep = '_'
    temp_list = [now, file_name]
    name = sep.join(temp_list)
    return name


def remove_set_from_list(inital_list, sellected_list):
    f_inital_list = inital_list.copy()
    f_sellected_list = sellected_list.copy()
    set_1 = set(f_inital_list)
    set_2 = set(f_sellected_list)
    updated_set = set_1.difference(set_2)
    return list(updated_set)


def return_date_string():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M'))


def datetime_error_handling(series):
    item_list = []
    for item in series:
        x = dateutil.parser.parse(item)
        if x.year < 2000:
            y = return_correct_year(x.year)
            x = x.replace(year=y)
        item_list.append(x)
    return pd.Series(item_list)


def return_correct_year(year):
    st = str(year)
    if st[-1] == '4':
        return 2014
    elif st[-1] == '5':
        return 2015


def remove_space_from_string(series):
    lst = []
    for item in series:
        if ' ' in item:
            item = item.replace(' ', '')
            lst.append(item)
        else:
            lst.append(item)
    return pd.Series(lst)


def localize_float_units(series):
    locale.setlocale(locale.LC_ALL, '')
    loc = locale.getlocale()
    lst = []
    for item in series:
        if loc[0] == 'en_US':
            x = item.replace(',', '.')
            lst.append(x)
    return pd.Series(lst)


def create_grouped_list(nr_of_groups, item_list):
    length = len(item_list)
    cell_size = get_cell_size(length, nr_of_groups)
    start = 0
    end = cell_size
    grp_columns = []
    for i in range(nr_of_groups):
        grp_columns.append(item_list[start:end])
        start = end
        end = end + cell_size
        if end > length:
            end = length
    return grp_columns


def create_list_from_data_frame_columns(df_columns):
    columns = []
    for item in df_columns:
        columns.append(item)
    return columns


def get_cell_size(length, columns):
    grp_size = length / columns
    return math.ceil(grp_size)


def update_list(datetime_list, columns_list, key):
    items_list = datetime_list.copy()
    for item in columns_list:
        if key in item:
            items_list.append(item)
    return items_list


class Categories:

    def __init__(self):
        super().__init__()
        self.presellected_items = ['Order No',
                                   'Sales Part No',
                                   'Sales Qty',
                                   'Customer No',
                                   'Promised Delivery Date/Time',
                                   'Price/Curr',
                                   'Sales Part Description',
                                   'Last Actual Ship Date',
                                   'Planned Ship Date/Time',
                                   'Supply Code',
                                   'Status',
                                   'Order Type',
                                   'Customer Name',
                                   'Coordinator',
                                   'Site',
                                   'Configurable',
                                   'Configuration ID',
                                   'Gross Amt/Curr',
                                   'Wanted Delivery Date/Time',
                                   'Sales Part Type',
                                   'Part No',
                                   'Purchase Part No',
                                   'Supplier',
                                   'Supply Site',
                                   'Cust Stat Grp',
                                   'SalesGroup',
                                   'Currency',
                                   'Currency Rate',
                                   'Price Source',
                                   'Price/Base',
                                   'Source Price/Curr',
                                   'Price incl Tax/Base',
                                   'Sales Price incl Tax/Curr',
                                   'Net Amt/Base',
                                   'Gross Amt/Base',
                                   'Net Amount/Curr',
                                   'Cost',
                                   'Total Cost/Base',
                                   'Target Date/Time',
                                   'Planned Delivery Date/Time',
                                   'Planned Due Date',
                                   'First Actual Ship Date',
                                   'Created',
                                   'Tax Liability',
                                   'Tax Code',
                                   'Tax Amount/Base',
                                   'Discount (%)',
                                   'Group Discount (%)',
                                   'Additional Discount (%)',
                                   'Total Order Line Discount (%)',
                                   'Delivery Type',
                                   'Demand Code',
                                   'Order Ref 1',
                                   'Customer Warranty',
                                   'Delivery Terms',
                                   'Del Terms Location',
                                   'Ship Via Code',
                                   'Confirmed Date',
                                   'Region Code',
                                   'Program ID',
                                   'Project ID',
                                   'Project Name',
                                   'Sub Project ID',
                                   'Sub Project Description',
                                   'Activity ID',
                                   'Activity Description',
                                   'Activity Sequence',
                                   'Cost Cent',
                                   'BusinessLi',
                                   'Counterpar',
                                   'Project',
                                   'Shopord',
                                   'Ext CO No',
                                   'Ext CO Site',
                                   'Eur Value',
                                   'Country of Origin',
                                   'Financial Project',
                                   'Price Incl Discount',
                                   'Total Cost Eur',
                                   'Customs Stat No']
        self.categorical_items = ['Supply Code',
                                  'Status',
                                  'Order Type',
                                  'Coordinator',
                                  'Site',
                                  'Sales Part Type',
                                  'Supplier',
                                  'Cust Stat Grp',
                                  'Currency',
                                  'Delivery Type',
                                  'Demand Code',
                                  'Customer Warranty',
                                  'Delivery Terms',
                                  'Region Code',
                                  'BusinessLi',
                                  'Country of Origin']
        self.datetime_items = ['Created']
        self.integer_items = ['Customs Stat No',
                              'Activity Sequence',
                              'Group Discount (%)',
                              'Discount (%)',
                              'Cost Cent']
        self.float_items = ['Price/Curr',
                            'Gross Amt/Curr',
                            'Currency Rate',
                            'Price/Base',
                            'Price incl Tax/Base',
                            'Net Amt/Base',
                            'Gross Amt/Base',
                            'Net Amount/Curr',
                            'Cost',
                            'Total Cost/Base',
                            'Eur Value',
                            'Price Incl Discount',
                            'Total Cost Eur']
        self.date_series = ['Year', 'Month']
        self.customer_app_preset = ['Customer No',
                                    'Eur Value',
                                    'Year',
                                    'Month']
        self.salespart_app_preset = ['Sales Part No',
                                     'Sales Qty',
                                     'Eur Value',
                                     'Year',
                                     'Month']
        self.site_app_preset = ['Site',
                                'Eur Value',
                                'Year',
                                'Month']
