import yaml

class FileLoader:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.load_date = None
        self.__load(self.__get_file_type())

    def __load(self,file_type):
        if file_type == 'yaml':
            self.__load_yaml()
            print("读取yaml文件")

    def __get_file_type(self):
        file_type = self.__file_path.split('.')[-1]
        return file_type

    # 读取config.yaml
    def __load_yaml(self):
        with open(self.__file_path, 'r', encoding='utf-8') as file:
            self.load_date = yaml.safe_load(file)
