import os

from core_func.env_manager import EnvLoader, EnvChecker, EnvInstaller, EnvUninstaller
from core_func.log_manager import LogLoader

MAIN_PATH = r'C:\AutoDeployToolsEnvs'
ZIP_PATH = r'C:\AutoDeployToolsEnvs\Downloads'
ENVS_PATH = r'C:\AutoDeployToolsEnvs\Envs'

class Runner:
    def __init__(self):
        print("Tip: 生成了Runner实例!")
        # print("Tip: 正在进行程序初始化!")
        directory_paths = [MAIN_PATH, ZIP_PATH, ENVS_PATH]
        for directory_path in directory_paths:
            os.makedirs(directory_path, exist_ok=True)
        self.eloader = EnvLoader()
        self.logloader = LogLoader()

    # 检测是否检测到已安装该环境 True-没检测到 , False-检测到了
    def __check_is_installed(self, env_name):
        echecker = EnvChecker(env_name, self.eloader, self.logloader.get_env_installed)
        return echecker.run_check()

    # 安装环境
    def __run_install_env(self, env_name):
        return EnvInstaller(env_name,self.eloader).return_installed_over

    # 更新日志 - 安装
    def __update_log_install(self, env_name):
        return self.logloader.add_env_installed(env_name)

    def Run_Installer(self, env_name):
        is_success = False
        if self.__check_is_installed(env_name):
            if self.__run_install_env(env_name):
                if self.__update_log_install(env_name):
                    is_success = True
        return is_success

    # 检查是否使用过该软件
    def __check_ware_used(self):
        return self.logloader.is_used

    # 更新日志 - 卸载
    def __update_log_uninstall(self,env_name):
        return self.logloader.del_env(env_name)

    # 卸载环境
    def __run_uninstall_env(self, env_name):
        return EnvUninstaller(env_name, self.eloader).return_uninstalled_over

    def Run_Uninstall(self, env_name):
        is_success = False
        if self.__check_ware_used():
            if self.__run_uninstall_env(env_name):
                if self.__update_log_uninstall(env_name):
                    is_success = True
        return is_success

    def Get_env_can_be_installed(self):
        return self.eloader.env_name_list

if __name__ == '__main__':
    Runner().Run_Installer(input("env_name?"))