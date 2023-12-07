from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
import random

sleep_time = random.uniform(1, 2)


# 크롬 디버거로 크롬 구동
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
time.sleep(3)  # 크롬이 완전히 실행될 때까지 대기

# 웹드라이버 설정
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = 'C:\\Users\\USER\\Downloads\\chromedriver_win32\\chromedriver.exe'
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(driver_path, options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(driver_path, options=option)

driver.implicitly_wait(5)  # 웹 자원 로드를 위해 5초까지 기다림

# CSV 파일 이름
csv_file_name = 'TM_11-04.csv'

# CSV 파일 읽기
df = pd.read_csv(csv_file_name)

# 파일 이름에서 '.csv' 앞의 부분만 추출
file_prefix = csv_file_name.split('.csv')[0]

# 추출한 부분에 "추천 리스트"를 붙임
final_string = f"{file_prefix}"

time.sleep(sleep_time)


# 샘플 코드로 삼성전자(005930) 종목에 접근하여 관심종목에 등록
driver.get('https://finance.naver.com/item/main.nhn?code=005930')
time.sleep(sleep_time)
driver.find_element(By.XPATH, '//*[@id="middle"]/div[1]/div[2]/p/a[1]').click()
time.sleep(sleep_time)
driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/p[1]/button').click()
time.sleep(sleep_time)

# 그룹명 입력
input_field = driver.find_element(By.CSS_SELECTOR, 'input.input_txt')
driver.execute_script(f"arguments[0].value = '{final_string}';", input_field)
time.sleep(sleep_time)
driver.find_element_by_css_selector('a._btn_add_ok').click()

# 종목을 순회하면서 관심종목에 등록
for ticker in df['Ticker']:
    ticker_str = str(ticker).zfill(6)
    print(f"Trying to navigate to the page of ticker: {ticker_str}")

    driver.get(f'https://finance.naver.com/item/main.nhn?code={ticker_str}')
    print(f"Current URL: {driver.current_url}")

    try:
        driver.find_element(By.XPATH, '//*[@id="middle"]/div[1]/div[2]/p/a[1]').click()
        time.sleep(sleep_time)

        # '관심종목 1' 그룹 선택
        driver.find_element(By.XPATH, f"//span[text()='{final_string}']").click()
        time.sleep(sleep_time)
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/p[2]/button[1]').click()
        print(f"Successfully added ticker: {ticker_str}")

    except Exception as e:
        print(f"Failed to add ticker: {ticker_str}, error: {e}")

time.sleep(sleep_time)
