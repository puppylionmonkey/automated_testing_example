import os
import shutil
import subprocess
import sys
import zipfile
import requests
from lxml import etree

from config1.path_config import project_path


# 自動下載對應版本chromedriver
# 取得chrome version
def get_chrome_version():
    chrome_version = ''
    if os_system == 'win32' or os_system == 'cygwin':  # windows
        command = ["wmic", "datafile", "where", 'name="C:/Program Files/Google/Chrome/Application/chrome.exe"', "get", "Version", "/value"]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        chrome_version = result.stdout.strip()
        chrome_version = chrome_version.replace('Version=', '')
    elif os_system == 'darwin':  # mac
        out_bytes = subprocess.check_output(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
        out_text = out_bytes.decode('utf-8')
        chrome_version = out_text.replace('Google Chrome ', '').strip()
    return chrome_version


def get_download_chromedriver_url():
    # 依照chrome版本取得對應chromedriver連結
    download_chromedriver_url = ''
    if os_system == 'win32' or os_system == 'cygwin':  # windows
        download_chromedriver_url = 'https://storage.googleapis.com/chrome-for-testing-public/' + chrome_version + '/win64/chromedriver-win64.zip'
    elif os_system == 'darwin':  # mac
        download_chromedriver_url = 'https://storage.googleapis.com/chrome-for-testing-public/' + chrome_version + '/mac-arm64/chromedriver-mac-arm64.zip'
    return download_chromedriver_url


def download_file(file_url, file_path):
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # 檢查是否有錯誤
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"檔案已下載並儲存為: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"下載失敗: {e}")


# 解壓 .zip 文件
def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"文件已解壓到: {extract_to}")


# 移動文件或目錄，若目標已存在則覆蓋
def move_file_or_directory(src, dest):
    try:
        # 如果目標已存在，先刪除
        if os.path.exists(dest):
            if os.path.isfile(dest) or os.path.islink(dest):
                os.remove(dest)  # 刪除文件或符號鏈接
            elif os.path.isdir(dest):
                shutil.rmtree(dest)  # 刪除目錄
        shutil.move(src, dest)
        print(f"文件或目錄已移動到: {dest}")
    except Exception as e:
        print(f"移動失敗: {e}")


# 刪除非空目錄
def delete_directory(dir_path):
    try:
        shutil.rmtree(dir_path)
        print(f"已刪除目錄及其內容: {dir_path}")
    except FileNotFoundError:
        print(f"目錄不存在: {dir_path}")
    except Exception as e:
        print(f"刪除失敗: {e}")


# 刪除文件
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"已刪除文件: {file_path}")
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
    except Exception as e:
        print(f"刪除失敗: {e}")


os_system = sys.platform

# 取得chrome版本
chrome_version = get_chrome_version()
download_chromedriver_url = get_download_chromedriver_url()
# 從chromedriver連結下載壓縮檔
zip_file_path = "chromedriver.zip"
download_file(download_chromedriver_url, zip_file_path)
# 解壓縮
unzip_file(zip_file_path, project_path)

# 移動chromedriver
chromedriver_folder_src = ''
ccc = ''
if os_system == 'win32' or os_system == 'cygwin':  # windows
    chromedriver_folder_src = project_path + 'chromedriver-win64'
    ccc = 'chromedriver.exe'
elif os_system == 'darwin':  # mac
    chromedriver_folder_src = project_path + 'chromedriver-mac-arm64'  # 要移動的文件或目錄
    ccc = 'chromedriver'

move_file_or_directory(chromedriver_folder_src + '/' + ccc, project_path + ccc)

# 刪除檔案
delete_directory(chromedriver_folder_src)
delete_file(project_path + 'chromedriver.zip')

if os_system == 'darwin':  # mac要解權限
    os.chmod(project_path + 'chromedriver', 755)
