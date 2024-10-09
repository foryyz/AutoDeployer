import os
import urllib
import zipfile
import subprocess
import yaml
from tqdm import tqdm


class EnvLoader:
    def __init__(self):
        self._env_list = self.__return_env_list()
        self._env_name_list = self.__return_env_name_list()
        print("正在初始化环境读取器...")
        directory_paths=['C:/AutoDeployToolsEnvs','C:/AutoDeployToolsEnvs/Downloads','C:/AutoDeployToolsEnvs/Envs']
        for directory_path in directory_paths:
            os.makedirs(directory_path, exist_ok=True)

    def __load_config(self):
        with open("config.yaml", 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def __return_env_list(self):
        config = self.__load_config()
        environments_dict={}
        for env in config.get('environments', []):
            name=env.get('name')
            version=env.get('version')
            url=env.get('url')
            download_path=env.get('download_path')
            install_path=env.get('install_path')
            env_path=env.get('env_path')
            check_way=env.get('check_way', {})
            # print("check_way : " , check_way)
            env_var=check_way.get('env_var', None)
            # print("env_var : " , env_var)
            default_paths=check_way.get('default_path', [])
            # print("default_paths : " , default_paths)

            # 将信息存储到字典中
            environments_dict[name]={
                'version': version,
                'url': url,
                'install_path': install_path,
                'download_path': download_path,
                'env_path' : env_path,
                'check_way': check_way,
                'env_var': env_var,
                'default_paths': default_paths
            }
        return environments_dict

    def __return_env_name_list(self):
        config=self.__load_config()
        env_name_list=[]
        for env in config.get('environments', []):
            name=env.get('name')
            env_name_list.append(name)
        return env_name_list

    def get_env_version(self, env_name):
        return self._env_list[env_name]['version']

    def get_env_download_path(self, env_name):
        return self._env_list[env_name]['download_path']

    def get_env_install_path(self, env_name):
        return self._env_list[env_name]['install_path']

    def get_env_path(self, env_name):
        return self._env_list[env_name]['env_path']

    def get_env_url(self, env_name):
        return self._env_list[env_name]['url']

    def get_env_var(self, env_name):
        return self._env_list[env_name]['env_var']

    def get_default_paths(self, env_name):
        return self._env_list[env_name]['default_paths']

    def get_env_check_type(self, env_name):# 识别检测模式
        if self.get_env_var(env_name) and self.get_env_path(env_name):
            return 1
        return 0


class EnvChecker:
    def __init__(self, env_name, eloadeR):
        self.env_name=env_name
        self.eload=eloadeR
        self.env_var = self.eload.get_env_var(env_name)
        print("正在准备环境检验器...")

    def check_env_var(self, env_name ,env_var):
        print("正在执行系统变量的检测...")
        env_value=os.getenv(env_var)
        if env_value:
            print(f"Environment variable {env_var} is set to {env_value}")
            return True
        else:
            print(f"未检测到系统变量 {env_var} ")
            return False

    def check_env_default_paths(self, env_name, paths):
        return

    def run_check(self):
        print("\n开始执行环境安装检测...")
        var=self.eload.get_env_var(self.env_name)
        default_paths=self.eload.get_default_paths(self.env_name)
        if var:
            print("\t- 系统变量检测")
            if self.check_env_var(self.env_name, self.env_var):
                print("已存在该环境")
                return True
        if default_paths:
            print("\t- 默认路径检测")

        return False

class EnvInstaller:
    def __init__(self, env_name, url, download_path, install_path, env_var=None,env_path=None):
        self.env_name=env_name
        self.url = url
        self.download_path = download_path
        self.install_path = install_path
        self.__download_zip()
        self.__extract_zip()
        if env_var and env_path:
            self.__env_install(env_var, env_path)



    def __download_zip(self):
        print("开始下载["+self.env_name+"]...")
        print("\t- 下载链接为: ",self.url)
        print("\t- 下载路径为: ",self.download_path)
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc= self.env_name+" 下载中") as t:
            def reporthook(block_num, block_size, total_size):
                if total_size > 0:
                    t.total=total_size
                    t.update(block_size * block_num - t.n)

            urllib.request.urlretrieve(self.url, self.download_path, reporthook)
        print("\n下载完成。")

    def __extract_zip(self):
        print("开始解压["+self.env_name+"]...")
        print("\t- 解压路径为 ", self.install_path)
        with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
            file_list=zip_ref.namelist()
            with tqdm(total=len(file_list), unit='file', desc="解压中") as t:
                for file in file_list:
                    zip_ref.extract(file, self.install_path)
                    t.update(1)
        print("\n解压完成。")

    def __env_install(self, env_var, env_path):
        e_var = env_var
        e_path = env_path
        print("开始部署环境变量...")
        print(f"设置{e_var}为: {env_path}")
        subprocess.run(["powershell", "-Command",
                        f"[System.Environment]::SetEnvironmentVariable('{e_var}', '{e_path}', 'User')"])

        print(f"添加{e_var}到系统PATH中...")
        subprocess.run(["powershell", "-Command",
                        f"$env:Path += ';{e_path}/bin'; [System.Environment]::SetEnvironmentVariable('Path', $env:Path, 'User')"])

        print("\n环境变量设置成功。")

    def env_uninstall(self, env_name, log_path = 'used.log'):
        pass
    def __env_uninstall(self, env_var, env_path):
        e_var=env_var
        e_path=env_path
        print("开始删除环境变量...")

        # 删除指定的环境变量
        print(f"删除环境变量 {e_var}...")
        subprocess.run(["powershell", "-Command",
                        f"[System.Environment]::SetEnvironmentVariable('{e_var}', $null, 'User')"])

        # 从系统PATH中删除对应路径
        print(f"从系统PATH中移除{e_path}/bin...")
        subprocess.run(["powershell", "-Command",
                        f"$env:Path = ($env:Path -split ';') -ne '{e_path}/bin' -join ';'; "
                        f"[System.Environment]::SetEnvironmentVariable('Path', $env:Path, 'User')"])

        print("\n环境变量删除成功。")

# if __name__ == '__main__':
#     eload = EnvLoader()
#     print("目前支持以下环境的一键部署: ")
#     for e_name in eload._env_name_list:
#         print("\t",e_name)
#     env_name = input("应用程序启动完成！\n请输入你要安装的环境昵称: ")
#
#     # env_var = eload.get_env_var(env_name)
#     # env_default_paths = eload.get_default_paths(env_name)
#     # print("\n变量初始化成功...")
#     #
#     # print("\n开始执行环境安装检测...")
#     # if env_var:
#     #     print("\t- 系统变量检测")
#     #     echeck.check_env_var(env_name,env_var)
#     # if env_default_paths:
#     #     print("\t- 默认路径检测")
#
#     echeck = EnvChecker(env_name)
#     echeck.run_check()