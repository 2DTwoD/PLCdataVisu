import datetime


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