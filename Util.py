# 执行安装环境 - env_name
from runner import Runner

# 执行安装环境 - env_name
def install_env(env_name):
    Runner().Run_Installer(env_name)

# 执行卸载环境 - env_name
def uninstall_env(env_name):
    Runner().Run_Uninstall(env_name)

# 获取支持安装的列表 - ['JDK', 'Maven']
def get_env_can_be_install_list():
    return Runner().Get_env_can_be_installed()
