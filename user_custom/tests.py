from selenium import webdriver
import json
import os
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

default_download_directory = str(os.path.dirname(os.path.abspath(__file__)))
# print(default_download_directory)
# os.environ['XDG_DOWNLOAD_DIR'] = default_download_directory
#
# os.system("xdg-user-dirs-update --set DOWNLOAD " + default_download_directory)
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# driver = webdriver.Chrome('/home/bright/Downloads/chromedriver')
# driver.get("https://www.python.org")
# print(driver.title)
# search_bar = driver.find_element_by_name("q")
# search_bar.clear()
# search_bar.send_keys("getting started with python")
# search_bar.send_keys(Keys.RETURN)
# print(driver.current_url)
# driver.close()
# download_location = '/home/bright/Downloads/insurance_pro'
chrome_options = webdriver.ChromeOptions()
# chrome_options.headless = True
# chrome_options.add_argument('--headless')
#
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": "",
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False,
    "isCssBackgroundEnabled": True,
}
prefs = {'download': {'default_directory': str(os.path.dirname(os.path.abspath(__file__))),
                      "directory_upgrade": True, "extensions_to_open": ""},
         'printing.print_preview_sticky_settings.appState': json.dumps(settings),
         # 'download.prompt_for_download': False,
         # 'download.directory_upgrade': True,
         # 'safebrowsing.enabled': False,
         # 'safebrowsing.disable_download_protection': True
         }
chrome_options.add_argument(
    "download.default_directory=" + str(os.path.dirname(os.path.abspath(__file__))))
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
CHROMEDRIVER_PATH = '/home/bright/Downloads/chromedriver'
with Display(backend="xvfb", size=(1920, 1080), color_depth=24) as disp:
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
    # params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': str(
    #     os.path.dirname(os.path.abspath(__file__)))}}
    # driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    # command_result = driver.execute("send_command", params)
    # print("response from browser:")
    # for key in command_result:
    #     print("result:" + key + ":" + str(command_result[key]))
    driver.get("https://test.peachesfinance.com/graph/4/")

    try:
        print("1")
        element = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.ID, "chart6"))
        )
        print(element)
    finally:
        driver.execute_script('window.print();')
        driver.quit()
