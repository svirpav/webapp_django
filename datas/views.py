from django.shortcuts import render
from . import toolbox
from . import application

tb = toolbox.Toolbox()


def main_view(requests):
    context = {}
    html_view = 'datas/main.html'
    if requests.method == 'POST':
        btn_response = requests.POST.get('btn')
        if btn_response == 'load':
            context['view'] = btn_response
        elif btn_response == 'send':
            try:
                file = requests.FILES['data']
                tb.create_raw_df(file)
                context['view'] = btn_response
                tb.create_raw_df_columns()
                context['ctx'] = tb.get_raw_df_columns()
            except KeyError:
                context['view'] = 'load'
        elif btn_response == 'sellect':
            q_dict = requests.POST
            sellected_items = tb.query_dict_to_list(q_dict)
            tb.save_sellected_columns(sellected_items)
            if sellected_items is not None:
                tb.create_app_list(sellected_items)
                context['ctx'] = tb.get_app_list()
                context['view'] = btn_response
            else:
                context['ctx'] = tb.get_raw_df_columns()
                context['view'] = 'send'
        elif btn_response in tb.get_app_list():
            context['view'] = btn_response
            if btn_response == 'Customer Analysis':
                tb.create_customer_list()
                context['customers'] = tb.get_customer_list()
                context['sellected_items'] = tb.get_sellected_list()
        elif btn_response == 'process-cust':
            keys = ['customer', 'sellected']
            response_dict = tb.query_dictionary_handler(requests.POST, keys)
            app = application.Customer(tb.get_data())
            app.application(response_dict)
        # END CONDITION
        elif btn_response == 'main':
            tb.clear_data()
            context['view'] = btn_response
        else:
            context['view'] = 'main'
    else:
        context['view'] = 'main'
    return render(requests, html_view, context)
