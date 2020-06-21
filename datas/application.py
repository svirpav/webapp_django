from . import toolbox


class Customer:

    def __init__(self, raw_data_frame):
        self.raw_data_frame = raw_data_frame
        self.tb = toolbox.Toolbox()

    def application(self, response_dict):
        for customer in response_dict['customer']:
            clean_data = \
                self.tb.return_cleaned_data(self.raw_data_frame,
                                            response_dict['sellected'])
            for customer in response_dict['customer']:
                customer_grp = \
                    self.tb.create_and_return_group(clean_data, customer)
                print(customer_grp)
