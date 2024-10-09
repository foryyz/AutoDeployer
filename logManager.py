import os

class LogLoader:
    def __init__(self, log_path='used.log'):
        self.log_path = log_path
        self.env_installed = []
        self.is_used = False
        if self.check_log_exist():
            print("检测到日志文件! 正在读取已安装的环境...")
            self.load_env_installed()
            if len(self.env_installed)>0:
                self.is_used = True
                print(f"\t- 读取到{len(self.env_installed)}个环境已被安装\n")
            else:
                print("\t- 未读取到使用该程序安装的环境！\n")

        else:
            print("未检测到日志文件!")


        print("成功加载日志器")

    def check_log_exist(self):
        # 检测文件是否存在
        if os.path.exists(self.log_path):
            return True
        return False

    #将文件中的行字符串 添加到数组中
    def load_env_installed(self):
        with open(self.log_path, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                if not line.strip() in self.env_installed:
                    self.env_installed.append(line.strip())

    def check_env_installed(self, env_name):
        if self.is_used:
            for env in self.env_installed:
                if env == env_name:
                    return True
        return False

    def add_env_installed(self, env_name):
        if env_name not in self.env_installed:
            with open(self.log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{env_name}\n")  # 每个字符串后面加换行符
                self.env_installed.append(env_name)