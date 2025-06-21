import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from config1.path_config import project_path, chrome_path
from functions.common_functions import extract_archive, pack_chrome_extension


class WebUser:
    def __init__(self, chromedriver_path=project_path + 'chromedriver', is_use_google_account=False, is_load_extension=False, un_pack_extension_zip_path='/Users/chuchengan/Desktop/coinwallet_int_android/web_prod_2.0.13(857).zip'):
        service = Service(executable_path=chromedriver_path)
        self.options = webdriver.ChromeOptions()
        if is_use_google_account:
            self.options.add_argument(r"user-data-dir=" + chrome_path)  # 使用chrome 帳號資料開啟# 不能同時開兩個
        if is_load_extension:
            un_pack_extension_dir = un_pack_extension_zip_path.replace('.zip', '')
            packed_extension_crx = un_pack_extension_zip_path.replace('.zip', '.crx')
            packed_extension_pem = un_pack_extension_zip_path.replace('.zip', '.pem')
            packed_extension_dir = un_pack_extension_zip_path.replace('.zip', '_packed')
            extract_archive(un_pack_extension_zip_path, un_pack_extension_dir)
            pack_chrome_extension(un_pack_extension_dir, packed_extension_pem)
            extract_archive(packed_extension_crx, packed_extension_dir)
            print(packed_extension_dir)
            self.options.add_argument(f"--load-extension={packed_extension_dir}")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument("--disable-extensions")
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 120)
        self.actions = ActionChains(self.driver)

    def wait_until_element_visible(self, xpath):
        self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))

    def wait_until_element_presence(self, xpath):
        self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))

    def scroll_down_until_element_visible_by_js(self, xpath):
        self.driver.execute_script("return arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, xpath))
        time.sleep(1)

    def scroll_down_until_element_visible_by_top(self, xpath):  # true: 頂端對齊
        self.driver.execute_script("return arguments[0].scrollIntoView(true);", self.driver.find_element(By.XPATH, xpath))
        time.sleep(1)

    def scroll_down_until_element_visible_by_bottom(self, xpath):  # false: 底端對底端
        self.driver.execute_script("return arguments[0].scrollIntoView(false);", self.driver.find_element(By.XPATH, xpath))
        time.sleep(1)
