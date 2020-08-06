''' UTILS '''
from datetime import datetime
import dateutil
import pandas as pd


def get_cell_size(length, columns):
    grp_size = length / columns
    return int(grp_size)


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


def create_file_name(date, sep, name):
    tmp = [date, name]
    name = sep.join(tmp)
    return name


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
