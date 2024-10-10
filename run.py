from envManager import EnvLoader, EnvChecker, EnvInstaller
from logManager import LogLoader

if __name__ == '__main__':
    eload=EnvLoader()
    logloader=LogLoader()

    print("目前支持以下环境的一键部署: ")
    for e_name in eload._env_name_list:
        print("\t", e_name)
    env_name=input("应用程序启动完成！\n请输入你要安装的环境昵称: ")

    echecker=EnvChecker(env_name, eload, logloader.get_env_installed)
    if echecker.run_check():
        print("\n开始执行安装程序!")
        if EnvInstaller(env_name, eload).return_installed_over:
            logloader.add_env_installed(env_name)# 更新日志
            print(f"\n程序执行完毕...\n\n恭喜您成功安装[{env_name}]！")
        else:
            print(f"\n可能发生了一些错误！\n\n[{env_name}]安装失败！")
