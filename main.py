import datetime

import matplotlib.pyplot as plt


plot_dict = {}


def get_data_from_file(file_path: str):
    result = {}
    error = ''
    try:
        f = open(file_path, 'r', encoding='utf-8')
        try:
            header = f.readline().split("; ")
            for item in header:
                key_value = item.split(": ")
                if len(key_value) == 2:
                    result[key_value[0]] = key_value[1]
            if len(result) != 10:
                raise Exception('Некорректный заголовок')
            result["values"] = []
            f.readline()
            while True:
                data = f.readline()
                if data == '':
                    break
                data = data.split(' | ')
                if len(data) != 5:
                    raise Exception('Некорректные данные')
                result["values"].append((datetime.datetime.fromtimestamp(float(data[1])), float(data[3])))
        except Exception as e:
            error = str(e)
        finally:
            f.close()
    except Exception as e:
        error = str(e)
    return result, error


def sort_fun(item):
    return item[0]


def append_plot_dict(file_name):
    data, error = get_data_from_file(file_name)
    if error != '':
        return error
    try:
        name = f"{data['ПЛК']}/{data['Переменная']}"
        if name not in plot_dict:
            plot_dict[name] = []

        for i in data['values']:
            plot_dict[name].append(i)

        plot_dict[name].sort(key=sort_fun)
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


def main():
    append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-37-43-605 total 3600.trnd')
    append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-30-24-997 total 3600.trnd')
    append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-44-59-563 total 3600.trnd')
    append_plot_dict('records/ПЛК/Переменная 1/05.02.2026 11-52-12-944 total 3600.trnd')
    append_plot_dict('records/ПЛК/Переменная 2/05.02.2026 11-30-24-999 total 3600.trnd')
    append_plot_dict('records/ПЛК/Переменная 9/05.02.2026 11-37-43-677 total 3600.trnd')
    append_plot_dict('records/ПЛК/Переменная 10/05.02.2026 11-30-25-015 total 3600.trnd')
    plt.figure(figsize=(12, 8))
    for key, val in plot_dict.items():
        x_list, y_list = get_xy(val)
        plt.plot(x_list, y_list, label=key)

    plt.ylabel('значение')
    plt.xlabel('время')
    plt.gcf().autofmt_xdate()
    plt.grid()
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
