import os
import json

library_dir = input("请输入图书馆根路径：")  # 图书馆的目录
library_dict = None


def category_name(code):
    """
    拼接类别名称
    :param code: 类别代码
    :return: eg. A 马列主义毛邓思想
    """
    if not code:
        return ""
    return code + " " + library_dict[code]


def read_categories_codes():
    """
    读取类别代码
    :return: [A, A1, ...]
    """
    file_name = "category_codes.txt"
    file_object = open(file_name)
    file_context = file_object.read()
    return file_context.split(",")


def read_categories_dict():
    """
    读取code与名称的dict
    :return: dict
    """
    file_name = "library_a_dict.json"
    file_object = open(file_name)
    json_object = json.load(file_object)
    return json_object


def category_code(name):
    """
    提取类别code
    :param name:
    :return: code
    """
    arr = name.split(" ")
    if len(arr) <= 1:
        return name
    return arr[0]


def fix_category_path(path):
    """
    补全类别的路径，没有名称的加上
    :param path:
    :return: xx/xxx/xxx/A 马列主义毛邓思想
    """
    base_name = os.path.basename(os.path.normpath(path))
    code = category_code(base_name)
    father_path = path[:(len(path) - len(base_name) - 1)]
    dir_with_name = os.path.join(father_path, category_name(code))
    return dir_with_name


def path_of_category(dir, code):
    """
    类别的全路径
    :param dir: 上一个类别的路径
    :param code: 类别代码
    :return: xx/xxx/xxx/A 马列主义毛邓思想
    """

    if dir == library_dir:
        return os.path.join(dir, code)

    base_name = os.path.basename(os.path.normpath(dir))
    upper_code = category_code(base_name)

    if code.startswith(upper_code):
        # 拼接路径，dir有可能带名称，有可能只是code
        dir_with_name = fix_category_path(dir)
        return os.path.join(dir_with_name, code)

    dir = dir[:(len(dir) - len(base_name) - 1)]
    return path_of_category(dir, code)


def create_category_folder(path):
    """
    创建类别文件夹，如果类别名称不全则补全
    :param path: 类别的路径
    :return: 类别文件夹全路径
    """
    dir_with_name = fix_category_path(path)
    if not os.path.exists(dir_with_name):
        os.makedirs(dir_with_name)
    return dir_with_name


def create_hierarchy(dir, codes_arr):
    """
    递归创建图书馆类别层级目录
    :param dir: 上一层目录
    :param codes_arr: 待创建的类别
    :return: None
    """
    if not codes_arr:
        return

    code = codes_arr[0]
    path_without_name = path_of_category(dir, code)
    path = create_category_folder(path_without_name)
    print(path)
    folders_remaining = codes_arr[1:]
    return create_hierarchy(path_without_name, folders_remaining)


def create_library():
    dir = library_dir
    codes_arr = read_categories_codes()

    while codes_arr:
        code = codes_arr[0]
        path_without_name = path_of_category(dir, code)
        path = create_category_folder(path_without_name)
        print(path)
        codes_arr = codes_arr[1:]
        dir = path_without_name


if __name__ == "__main__":
    library_dict = read_categories_dict()
    create_library()
    # codes_arr = read_categories_codes()
    # library_dict = read_categories_dict()
    # if os.path.isdir(library_dir):
    #     create_hierarchy(library_dir, codes_arr)
    # else:
    #     print("您输入的不是一个路径")
