from . import utils
from . import data
import pandas as pd


class PepareData(data.BaseDataHandling):

    @staticmethod
    def _to_string(data, exclude_list):
        loc_data = data.copy(deep=True)
        items_list =\
            utils.create_list_from_data_frame_columns(loc_data.columns)
        error_list = []
        for item in items_list:
            if item not in exclude_list:
                try:
                    loc_data[item] = loc_data[item].astype('string')
                except ValueError as err:
                    print(err, ':', item)
                    error_list.append(item)
        return loc_data

    @staticmethod
    def _to_categorical(data, category_list):
        loc_data = data.copy(deep=True)
        items_list =\
            utils.create_list_from_data_frame_columns(loc_data.columns)
        for item in category_list:
            if item in items_list:
                loc_data[item] = loc_data[item].astype('category')
        return loc_data

    @staticmethod
    def _to_datetime(data, items_list):
        loc_data = data.copy(deep=True)
        datetime_list = items_list.copy()
        columns_list =\
            utils.create_list_from_data_frame_columns(loc_data.columns)
        datetime_list = utils.update_list(datetime_list, columns_list, 'Date')
        error_list = []
        for item in datetime_list:
            try:
                loc_data[item] = loc_data[item].astype('object')
                loc_data[item] = loc_data[item].astype('datetime64')
            except ValueError as err:
                print(format(err), ':', item)
                error_list.append(item)
        for error in error_list:
            loc_data[error] = utils.datetime_error_handling(loc_data[error])
            loc_data[error] = loc_data[error].astype('datetime64')
        return loc_data

    @staticmethod
    def _to_int(data, int_list):
        loc_data = data.copy(deep=True)
        items_list =\
            utils.create_list_from_data_frame_columns(loc_data.columns)
        error_items_list = []
        for item in int_list:
            if item in items_list:
                if loc_data[item].isna().any():
                    loc_data[item] = loc_data[item].fillna('0')
                try:
                    loc_data[item] = loc_data[item].astype('int')
                except ValueError as err:
                    print(format(err))
                    error_items_list.append(item)
        return loc_data

    @staticmethod
    def _to_float(data, float_list):
        loc_data = data.copy(deep=True)
        items_list =\
            utils.create_list_from_data_frame_columns(loc_data.columns)
        error_list = []
        for item in float_list:
            if item in items_list:
                try:
                    loc_data[item] = loc_data[item].astype('float')
                except ValueError as err:
                    print(format(err), ':', item)
                    error_list.append(item)
        for error in error_list:
            loc_data[error] = utils.remove_space_from_string(loc_data[error])
            loc_data[error] = utils.localize_float_units(loc_data[error])
            loc_data[error] = loc_data[error].astype('float')
        return loc_data

    @staticmethod
    def _create_date_series(series, name):
        items_list = []
        for item in series:
            if name == 'Year':
                items_list.append(int(item.strftime('%Y')))
            elif name == 'Month':
                items_list.append(int(item.strftime('%m')))
        return pd.Series(items_list)


class DataCategories:

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
