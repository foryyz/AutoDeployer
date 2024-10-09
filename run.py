import os

from envManager import EnvLoader, EnvChecker, EnvInstaller
from logManager import LogLoader

if __name__ == '__main__':
    eload=EnvLoader()
    logloader=LogLoader()
    print("目前支持以下环境的一键部署: ")
    for e_name in eload._env_name_list:
        print("\t", e_name)
    env_name=input("应用程序启动完成！\n请输入你要安装的环境昵称: ")
    env_url = eload.get_env_url(env_name)
    env_download_path = eload.get_env_download_path(env_name)
    env_install_path = eload.get_env_install_path(env_name)
    env_var = eload.get_env_var(env_name)
    env_path = eload.get_env_path(env_name)

    echecker=EnvChecker(env_name, eload)
    if not echecker.run_check():
        print("\n开始执行安装程序!")
        # input("\n输入任意键开始执行安装程序！")
        if eload.get_env_check_type(env_name) == 0:
            einstaller = EnvInstaller(env_name, env_url, env_download_path, env_install_path)
        elif eload.get_env_check_type(env_name) == 1:
            einstaller=EnvInstaller(env_name, env_url, env_download_path,env_install_path, env_var, env_path)
        logloader.add_env_installed(env_name)

    print(f"\n程序执行完毕...\n\n恭喜您成功安装[{env_name}]！")
    # os.system('pause')