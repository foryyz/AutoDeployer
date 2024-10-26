import os
import urllib.request
import zipfile
import subprocess
from tqdm import tqdm

CONFIG_YAML = "config.yaml"

from file_loader import FileLoader

class EnvLoader:
    def __init__(self, CONFIG_YAML = CONFIG_YAML):
        self.config = FileLoader(CONFIG_YAML).load_date
        self.config_dict = self.__get_config_dict() # 将config文件转化为字典格式存储
        self.env_name_list = self.__get_env_name_list() # 读取可以安装的环境列表
        print("Tip: 正在初始化config读取器...")

    def __get_config_dict(self):
        # 使用FileLoader读取配置文件
        config_dict = {}
        for env in self.config.get('environments', []):
            name = env.get('name')
            version = env.get('version')
            url = env.get('url')

            zip_path = env.get('path')['zip_path']
            ENVS_PATH = env.get('path')['ENVS_PATH']
            env_path = env.get('path')['env_path']

            env_key = env.get('env_key', {})
            env_var = env_key.get('env_var', None)
            bin_paths = env_key.get('bin_paths', [])
            # default_paths=env_key.get('default_path', [])# 暂时移除对默认路径的检测

            # 将信息存储到字典中
            config_dict[name] = {
                'version': version,
                'url': url,
                'ENVS_PATH': ENVS_PATH,
                'zip_path': zip_path,
                'env_path': env_path,
                'env_key': env_key,
                'env_var': env_var,
                'bin_paths': bin_paths
                # 'default_paths': default_paths
            }
        return config_dict
    def __get_env_name_list(self):
        env_name_list=[]
        for env in self.config.get('environments', []):
            name=env.get('name')
            env_name_list.append(name)
        return env_name_list

    def get_env_download_url(self, env_name):
        return self.config_dict[env_name]['url']
    def get_env_version(self, env_name):
        return self.config_dict[env_name]['version']
    def get_env_zip_path(self, env_name):
        return self.config_dict[env_name]['zip_path']
    def get_ENVS_PATH(self, env_name):
        return self.config_dict[env_name]['ENVS_PATH']
    def get_env_path(self, env_name):
        return self.config_dict[env_name]['env_path']
    def get_env_key(self, env_name):
        return self.config_dict[env_name]['env_key']
    def get_env_var(self, env_name):
        return self.config_dict[env_name]['env_var']
    def get_bin_paths(self, env_name):
        return self.config_dict[env_name]['bin_paths']
    def get_env_install_type(self, env_name):# 识别检测模式
        if self.get_env_key(env_name):
            #如果env_key值不为空，则为系统变量模式
            return "env_key"
        return 0
    # 暂时移除对默认路径的检测
    # def get_default_paths(self, env_name):
    #     return self._env_list[env_name]['default_paths']

class EnvChecker:
    # env_installed由log_loader.py提供
    def __init__(self, env_name, eloader, env_installed_log):
        self.env_name=env_name
        self.eloader=eloader
        self.env_installed_log=env_installed_log
        self.env_var = self.eloader.get_env_var(env_name)

        print("Tip: 正在准备环境检验器...")


    @staticmethod
    def check_env_var(env_var):
        # 先来检测 env_var 是不是多个，多个则循环检测
        if isinstance(env_var, list):
            for e_v in env_var:
                for k in e_v.keys():
                    env_value=os.getenv(k)
        elif isinstance(env_var, str):
            env_value=os.getenv(env_var)
        else:
            print("type(env_var)",type(env_var))
            print("ERROR: env_var类型错误!")
            exit(1)

        if env_value:
            print(f"Environment variable {env_var} is set to {env_value}")
            return True
        else:
            print(f"\t\t→ 未检测到系统变量 {env_var} ")
            return False

    def __check_env_installed(self, env_name):
        if env_name in self.env_installed_log:
            # 如果安装过 则返回False
            return False
        return True
    # 暂时移除对默认路径的检测
    # def check_env_default_paths(self, env_name, paths):
    #     return

    # true表示正常，没有安装过环境
    def run_check(self):
        print("开始执行环境安装检测...")
        var=self.eloader.get_env_var(self.env_name)
        # default_paths=self.eload.get_default_paths(self.env_name)
        if not self.__check_env_installed(self.env_name):
            print("检测到已安装过该程序")
            return False

        # 只有当env_var存在时才执行系统变量检测
        if var:
            print("\t- 系统变量检测")
            if self.check_env_var(self.env_var):
                print("已存在该环境")
                return False
        # 暂时移除对默认路径的检测
        # if default_paths:
        #     print("\t- 默认路径检测")
        return True

class EnvInstaller:
    def __init__(self, env_name, eloader):
        self.env_name=env_name
        self.installed_over = False
        self.url = eloader.get_env_download_url(self.env_name)
        self.zip_path = eloader.get_env_zip_path(self.env_name)
        self.ENVS_PATH = eloader.get_ENVS_PATH(self.env_name)
        env_install_type=eloader.get_env_install_type(self.env_name)
        if env_install_type == "env_key":
            self.__download_zip()
            self.__extract_zip()
            self.__env_key_install(eloader.get_env_var(self.env_name), eloader.get_env_path(self.env_name), eloader.get_bin_paths(self.env_name))
            self.installed_over = True
        elif env_install_type == 0:
            print("该环境不包含env_key")
        else:
            print("没有此类安装模式!")

    def __download_zip(self):
        print("\n开始下载[" + self.env_name + "]...")

        if os.path.isfile(self.zip_path):
            print("\t- 检测到您已下载该环境压缩包！")
        else:
            print("\t- 下载链接为: ", self.url)
            print("\t- 压缩包路径为: ", self.zip_path)
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=self.env_name + " 下载中") as t:
                def reporthook(block_num, block_size, total_size):
                    if total_size > 0:
                        t.total=total_size
                        t.update(block_size * block_num - t.n)

                urllib.request.urlretrieve(self.url, self.zip_path, reporthook)
        print("下载完成。")

    def __extract_zip(self):
        print("\n开始解压["+self.env_name+"]...")
        print("\t- 解压路径为 ", self.ENVS_PATH)
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            file_list=zip_ref.namelist()
            with tqdm(total=len(file_list), unit='file', desc="解压中") as t:
                for file in file_list:
                    zip_ref.extract(file, self.ENVS_PATH)
                    t.update(1)
        print("解压完成")

    # 设置环境变量和Path的方法
    @staticmethod
    def __env_key_install(env_var, env_path, bin_paths):
        print("\n开始部署环境变量...")
        # print(f"设置{env_var}为: {env_path}")
        # print("DEBUG: env_var: ",env_var)
        if isinstance(env_var,list):
            print("\t- 检测到需要添加多个环境变量")
            for e_v in env_var:
                for k,v in e_v.items():
                    print(f"\t\t- 正在设置环境变量{k}")
                    subprocess.run(["powershell", "-Command",
                                f"[System.Environment]::SetEnvironmentVariable('{k}', '{v}', 'User')"])

        elif isinstance(env_var,str):
            print("\t- 检测到单个环境变量")
            subprocess.run(["powershell", "-Command",
                            f"[System.Environment]::SetEnvironmentVariable('{env_var}', '{env_path}', 'User')"])


        now_paths = subprocess.run(["powershell", "-Command",
                                   r'[System.Environment]::GetEnvironmentVariable("Path",[System.EnvironmentVariableTarget]::User)'],
                                  text=True, capture_output=True, shell=True).stdout[:-1]

        over_bin_path="".join(b for b in bin_paths)
        print(f"\t- 添加[{over_bin_path}]到系统PATH中...")
        env_real_var = now_paths + over_bin_path
        subprocess.run(["powershell", "-Command",
                        f"[System.Environment]::SetEnvironmentVariable('Path', '{env_real_var}', [System.EnvironmentVariableTarget]::User)"])
        # 失败算法 ↓
        # subprocess.run(["powershell", "-Command", f"[System.Environment]::SetEnvironmentVariable('Path', $env:PATH+';{env_path}', [System.EnvironmentVariableTarget]::User)"], shell=True)
        print("环境变量设置成功。")

    @property
    def return_installed_over(self):
        return self.installed_over

class EnvUninstaller:
    def __init__(self, env_name, eloader):
        print("Tip: 开始执行环境卸载...")
        self.env_name = env_name
        self.uninstalled_over=False
        env_install_type=eloader.get_env_install_type(self.env_name)
        if env_install_type == "env_key":
            # print("\t- 执行环境变量卸载")
            self.__env_key_uninstall(eloader.get_env_var(self.env_name), eloader.get_bin_paths(self.env_name))
            self.uninstalled_over=True
        elif env_install_type == 0:
            print("\n\t\tDEBUG: 这个环境的的install_type=0")
        else:
            pass

    def __env_key_uninstall(self, env_var, bin_paths):
        print("Tip: 开始删除环境变量...")
        # print("DEBUG: bin_paths的值为: ", bin_paths)
        if isinstance(env_var,list):
            print("\t- 检测到需要清理多个环境变量")
            for e_v in env_var:
                for k in e_v.keys():
                    print(f"\t\t- 正在清理环境变量{k}")
                    subprocess.run(["powershell", "-Command",
                                    f"[System.Environment]::SetEnvironmentVariable('{k}', $null, 'User')"])
        elif isinstance(env_var,str):
            print("\t- 检测到单个环境变量")
            subprocess.run(["powershell", "-Command", f"[System.Environment]::SetEnvironmentVariable('{env_var}', $null, 'User')"])
        else:
            print("ERROR: 未知错误!")
            exit(1)
        # 从系统PATH中删除对应路径
        print(f"\t- 从系统PATH中移除{''.join(b for b in bin_paths)}...")
        # 获取系统变量 PATH 的值
        real_paths = subprocess.run(["powershell", "-Command",r'[System.Environment]::GetEnvironmentVariable("Path",[System.EnvironmentVariableTarget]::User)'], text=True, capture_output=True, shell=True).stdout
        read_path_list = real_paths.split(';')
        del read_path_list[-1] # 最后一个元素是换行符 要删除 不然会多一个;

        if isinstance(bin_paths,list):
            # print("检测到多个bin_path")
            use_bin_paths=[bin_path.replace(';', '') for bin_path in bin_paths]  # 要先去掉分号才能进行比较
        else:
            # print("检测到一个bin_path")
            use_bin_paths = bin_paths.replace(';', '')

        # print("DEBUG: use_bin_paths:", use_bin_paths)
        over_path = ""
        for read_path in read_path_list:
            # print("正在检查的是："+read_path)
            if read_path not in use_bin_paths:
                # print("DEBUG: 放行")
                over_path+=read_path + ";"
            else:
                # print("\t不放行")
                print("\t\t→ 成功在PATH变量中找到并删除一个!")

        # over_path = over_path[:-1] # 最后一个字符是; 需要删除 #已优化为不需要删除

        subprocess.run(["powershell", "-Command", f"[System.Environment]::SetEnvironmentVariable('Path', '{over_path}', [System.EnvironmentVariableTarget]::User)"], shell=True)
        print("Tip: 环境变量删除成功。")

    @property
    def return_uninstalled_over(self):
        return self.uninstalled_over