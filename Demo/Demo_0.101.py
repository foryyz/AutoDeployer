import os
import subprocess
import urllib.request
import zipfile
from tqdm import tqdm

"""
Demo_0.100
    - 实现了基础的 下载 压缩 添加环境变量的功能
    
Demo_0.101
    - 实现了下载和压缩的进度条显示

存在问题：
    - 路径的提取并不准确
"""


#检查JDK环境是否配置
def check_jdk_installed():
    java_home=os.getenv("JAVA_HOME")
    if java_home:
        print(f"JDK已安装，路径: {java_home}")
        return True
    else:
        print("未检测到JDK安装。")
        return False


def download_jdk():
    jdk_url="https://download.oracle.com/java/23/latest/jdk-23_windows-x64_bin.zip"
    jdk_zip_path="../jdk.zip"
    print("开始下载JDK...")

    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc="JDK 下载中") as t:
        def reporthook(block_num, block_size, total_size):
            if total_size > 0:
                t.total=total_size
                t.update(block_size * block_num - t.n)

        urllib.request.urlretrieve(jdk_url, jdk_zip_path, reporthook)
    print("\n下载完成。")


def extract_jdk(zip_path, extract_to):
    print("正在解压JDK...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list=zip_ref.namelist()
        with tqdm(total=len(file_list), unit='file', desc="解压中") as t:
            for file in file_list:
                zip_ref.extract(file, extract_to)
                t.update(1)
    print("JDK解压完成。")


def set_env_variables():
    jdk_path=os.path.abspath("jdk/jdk-23")
    print(f"设置JAVA_HOME为: {jdk_path}")
    subprocess.run(["powershell", "-Command",
                    f"[System.Environment]::SetEnvironmentVariable('JAVA_HOME', '{jdk_path}', 'User')"])

    print("添加JDK到系统PATH中...")
    subprocess.run(["powershell", "-Command",
                    f"$env:Path += ';{jdk_path}/bin'; [System.Environment]::SetEnvironmentVariable('Path', $env:Path, 'User')"])

    print("环境变量设置成功。")


def verify_jdk_installation():
    try:
        result=subprocess.run(["java", "-version"], capture_output=True, text=True)
        if "version" in result.stderr:
            print("JDK安装成功:", result.stderr.splitlines()[0])
        else:
            print("JDK安装失败。")
    except Exception as e:
        print("无法验证JDK安装:", e)


if __name__ == "__main__":
    if not check_jdk_installed():
        download_jdk()
        extract_jdk("../jdk.zip", "jdk")
        set_env_variables()
    verify_jdk_installation()
    os.system("pause")