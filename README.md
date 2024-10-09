> 项目开始时间: 2024/10/08
>
> 项目成员: yyz
>
> 最新更新时间: 2024/10/10
>
> 版本号: a0.110

# AutoDeployer

**a0.100**

**项目目的：实现一键的全自动Windows环境部署**

# 项目结构

### run.py - RUN Install - 执行环境安装

#### envManager.py - 目前的主要运行类

- **EnvLoader**
- **EnvChecker**
- **EnvInstaller**

#### logManager.py - 读取used.log文件

- **LogLoader** - 书写使用程序安装过的环境

#### config.yaml - 主要的环境安装配置文件

#### used.log - 保存使用该程序安装过的环境



# 更新日志

```
# - 表示新增加的功能
# / 表示发现的BUG

a0.100	yyz
	- 实现JDK环境的安装测试
	- 实现对使用程序的系统进行环境是否已安装的检测
	- 实现对已安装的程序进行日志生成
	- 实现对不同环境的不同安装管理→config.yaml
	
a0.110	yyz
	- 实现软件安装后的卸载功能→runUninstall.py
	- 卸载功能正常,成功删除了[env_var]和在[PATH]中追加的内容
		/会在PATH中遗留重复的内容
	- 更新对应日志生成
	/ [env_var] EnvCheck系统已存在变量的检测存在问题
	/ 添加环境变量的算法存在重复添加原本值的问题;
		/-问题原因 powershell不会主动刷新$env:PATH的值
		/-解决方法 直接对通过powershell对底层进行调用 刷新环境变量$env:?的值
```



# Python环境

version=3.12.2

- tqdm
- pyyaml



# 附录：

## 1 subprocess库

```python
env_var = "JAVA_HOME"
result = subprocess.run(["powershell", "-Command",f'echo $env:{env_var}'], capture_output=True, text=True, shell=True)
value = result.stdout.strip()

#对于subprocess.run的参数：
#	- capture_output=True/False 表示是否将返回输出保存到 stdout,如果设置否则直接输出到控制台
#	- text=True/False 表示返回值为文本
#	- shell=True 允许你在 shell 中执行命令，支持使用 shell 的功能

```



## 2 相关PowerShell指令

```powershell
#查找名为JAVA_HOME的环境变量(当前用户)
Get-ChildItem Env:JAVA_HOME

#显示变量PATH的值(当前用户)
$env:PATH

#设置环境变量的值
#其中第三个参数[System.EnvironmentVariableTarget]::Target指定了作用范围
#Machine-系统级别,所有用户 ; User-当前用户级别 ; Process-当前进程级
[System.Environment]::SetEnvironmentVariable("VariableName", "Value", [System.EnvironmentVariableTarget]::Target)


#查看系统环境变量 - 版本低无法使用
#Get-ChildItem Env: -Scope PATH

```

### 手动更新/刷新环境变量

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
```

