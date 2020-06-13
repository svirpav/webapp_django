from django.shortcuts import render
from . import toolbox

tb = toolbox.DataHandler()


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
                tb.save_file_as_df(file)
                context['ctx'] = tb.return_df_col_names()
                html_view = 'datas/sellect.html'
            except KeyError:
                html_view = 'datas/load_file.html'
        elif btn_response == 'sellect':
            q_dict = requests.POST
            sellected_items = tb.q_dict_handler(q_dict)
            tb.save_sellected_columns(sellected_items)
            if sellected_items is not None:
                app_list = tb.create_app_list(sellected_items)
                context['ctx'] = app_list
                html_view = 'datas/app.html'
            else:
                context['ctx'] = tb.get_raw_df_columns()
                html_view = 'datas/sellect.html'
        elif btn_response in tb.get_app_list():
            html_view = 'datas/app_handler.html'
        # END CONDITION
        elif btn_response == 'main':
            html_view = 'datas/main.html'
        else:
            html_view = 'datas/main.html'
    else:
        context['view'] = 'main'
        html_view = 'datas/main.html'
    return render(requests, html_view, context)
