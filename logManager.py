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
        self.is_used = True

    def del_env(self, env_name):
        try:
            self.env_installed.remove(env_name)
            # 创建一个临时列表来存储不包含目标字符串的行
            updated_lines=[]
            # 读取文件并检查每一行
            with open(self.log_path, 'r', encoding='utf-8') as log_file:
                for line in log_file:
                    # 如果当前行不包含目标字符串，则添加到临时列表
                    if env_name not in line:
                        updated_lines.append(line)

            # 将更新后的内容写回文件
            with open(self.log_path, 'w', encoding='utf-8') as log_file:
                log_file.writelines(updated_lines)
            return True
        except ValueError:
            #捕获 ValueError 异常，执行其他操作
            print("ERROR! 未在日志中找到该环境!")
            return False


    def show_env_installed(self):
        print("检测到您使用该软件安装了以下环境： ")
        for env in self.env_installed:
            print(env)