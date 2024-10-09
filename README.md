> 项目开始时间: 2024/10/08
>
> 项目成员: yyz
>
> 最新更新时间: 2024/10/09
>
> 版本号: a0.100

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

#### 

## 更新日志

```
a0.100	yyz
	- 实现JDK环境的安装测试
	- 实现对使用程序的系统进行环境是否已安装的检测
	- 实现对已安装的程序进行日志生成
	- 实现对不同环境的不同安装管理→config.yaml
```



# Python环境

version=3.12.2

- tqdm
- pyyaml
