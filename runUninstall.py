import os

from envManager import EnvLoader, EnvUninstaller
from logManager import LogLoader

if __name__ == '__main__':
    eload=EnvLoader()
    logloader=LogLoader()
    if logloader.is_used:
        logloader.show_env_installed()
    env_name = input("您需要卸载的环境昵称是: ")
    env_var = eload.get_env_var(env_name)
    env_path = eload.get_env_path(env_name)
    eUninstall = EnvUninstaller(env_name, env_var, env_path)

    if logloader.del_env(env_name):
        print("日志更新成功！")

    print(f"\n程序执行完毕...\n\n您已成功卸载[{env_name}]！")
    # os.system('pause')