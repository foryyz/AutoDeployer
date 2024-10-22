import os

from env_manager import EnvLoader, EnvChecker, EnvInstaller
from log_manager import LogLoader
import Util

def init():
    print("Tip: 正在进行程序初始化!")
    directory_paths = [Util.MAIN_PATH, Util.ZIP_PATH, Util.ENVS_PATH]
    for directory_path in directory_paths:
        os.makedirs(directory_path, exist_ok=True)

if __name__ == '__main__':
    init()

    eloader=EnvLoader()
    logloader=LogLoader()

    print("目前支持以下环境的一键部署: ")
    for e_name in eloader.env_name_list:
        print("\t", e_name)
    env_name=input("Tip: 应用程序启动完成！\n请输入你要安装的环境昵称: ")

    echecker=EnvChecker(env_name, eloader, logloader.get_env_installed)
    if echecker.run_check():
        print("Tip: 开始执行安装程序!")
        if EnvInstaller(env_name, eloader).return_installed_over:
            logloader.add_env_installed(env_name)# 更新日志
            print(f"\nSuccess: 程序执行完毕.\n恭喜您成功安装[{env_name}]！")
        else:
            print(f"\n可能发生了一些错误！\n[{env_name}]安装失败！")
