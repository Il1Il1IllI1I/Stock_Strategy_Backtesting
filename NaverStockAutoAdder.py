from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By


# 크롬 디버거로 크롬 구동
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
time.sleep(3)  # 크롬이 완전히 실행될 때까지 대기

# 웹드라이버 설정
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(driver_path, options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(driver_path, options=option)

driver.implicitly_wait(5)  # 웹 자원 로드를 위해 5초까지 기다림

# CSV 파일 읽기
df = pd.read_csv('TurtleMinervini_09-16.csv')

# 네이버 로그인 페이지 접속
driver.get('https://nid.naver.com/')
time.sleep(3)

# 관심종목 등록을 위한 기본 설정
current_date = datetime.now().strftime("%Y-%m-%d")
final_string = f"{current_date} 추천 리스트"

# 샘플 코드로 삼성전자(005930) 종목에 접근하여 관심종목에 등록
driver.get('https://finance.naver.com/item/main.nhn?code=005930')
driver.find_element(By.XPATH, '//*[@id="middle"]/div[1]/div[2]/p/a[1]').click()
driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/p[1]/button').click()
time.sleep(2)

# 그룹명 입력
input_field = driver.find_element(By.CSS_SELECTOR, 'input.input_txt')
driver.execute_script(f"arguments[0].value = '{final_string}';", input_field)
driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[1]/ul/li[4]/a[1]').click()

# 종목을 순회하면서 관심종목에 등록
for ticker in df['Ticker']:
    ticker_str = str(ticker).zfill(6)
    print(f"Trying to navigate to the page of ticker: {ticker_str}")

    driver.get(f'https://finance.naver.com/item/main.nhn?code={ticker_str}')
    print(f"Current URL: {driver.current_url}")

    try:
        driver.find_element(By.XPATH, '//*[@id="middle"]/div[1]/div[2]/p/a[1]').click()
        time.sleep(1)

        # '관심종목 1' 그룹 선택
        driver.find_element(By.XPATH, f"//span[text()='{final_string}']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/p[2]/button[1]').click()
        print(f"Successfully added ticker: {ticker_str}")

    except Exception as e:
        print(f"Failed to add ticker: {ticker_str}, error: {e}")

    time.sleep(2)