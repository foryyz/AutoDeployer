from envManager import EnvLoader, EnvUninstaller
from logManager import LogLoader

if __name__ == '__main__':
    eload=EnvLoader()
    logloader=LogLoader()
    if not logloader.is_used:
        print("您没有使用该软件安装过环境！")
        exit(1)
    logloader.show_env_installed()
    env_name = input("您需要卸载的环境昵称是: ")
    env_var = eload.get_env_var(env_name)
    env_path = eload.get_env_path(env_name)
    if EnvUninstaller(env_name, eload).return_uninstalled_over:
        if logloader.del_env(env_name):
            print("日志更新成功！")
        else:
            print("ERROR: 日志更新失败！")
        print(f"\n程序执行完毕...\n\n您已成功卸载[{env_name}]！")
    else:
        print(f"\n可能发生了一些错误！\n\n[{env_name}]卸载失败！")


