from asse.Btn import Btn, BtnType, BtnIcon


class ProductItem():
    def __init__(self, name, icon_path, env_path, type):
        self.name = name
        self.icon_path = icon_path
        self.nums = 0
        if type == BtnType.DOWNLOAD.value:
            self.btn = Btn(BtnIcon.DOWNLOAD.value, BtnType.DOWNLOAD.value, BtnType.DOWNLOAD.value,env_path)
        elif type == BtnType.DELETE.value:
            self.btn = Btn(BtnIcon.DELETE.value, BtnType.DELETE.value, BtnType.DELETE.value,env_path)
