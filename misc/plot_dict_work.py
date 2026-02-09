from misc.file_work import get_data_from_file


def sort_fun(item):
    return item[0]


def append_plot_dict(plot_dict_item: dict, file_name: str):
    data, error = get_data_from_file(file_name)
    if error != '':
        return error
    try:
        name = f"{data['ПЛК']}/{data['Переменная']}"
        if name not in plot_dict_item:
            plot_dict_item[name] = []

        for i in data['values']:
            plot_dict_item[name].append(i)

        plot_dict_item[name].sort(key=sort_fun)
    except Exception as e:
        error = str(e)
    return error


def get_xy(plot_dict_item):
    x_list = []
    y_list = []
    for item in plot_dict_item:
        x_list.append(item[0])
        y_list.append(item[1])
    return x_list, y_list