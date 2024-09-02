#main.py
import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
service = Service()

# AM 09 Web 접속 function 
def access():
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.sjraycastle.com/Member/LogIn.aspx")
       
    id = 'drjins7199'
    pw = 'rlarnrwls!12'
    #id = '50947200'
    #pw = '0000'
    weekVal = '2' #세로(주차값)
    dayVal = '2'  #가로(요일값) 1.일 2.월 
    courseVal = '1' # 1:세종, 2:레이, 3:캐슬
    teeVal = '2'    # 2~18 # 2~7
    buVal = '1'    # 1: 1부, 2: 2부 

    WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.ID, 'contents_txtId')))
    elem_id = driver.find_element(By.ID,'contents_txtId')
    elem_id.send_keys(id) # id 입력

    WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.ID,'contents_txtPwd')))
    elem_pw = driver.find_element(By.ID,'contents_txtPwd')
    elem_pw.send_keys(pw) #pw입력

    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, 'contents_lnkBtnLogin')))
    elem_btn = driver.find_element(By.ID, 'contents_lnkBtnLogin')
    elem_btn.click() # 로그인 버튼 클릭=> 로그인으로 이동
    time.sleep(1)

    #예약사이트로 이동
    driver.get('https://www.sjraycastle.com/Golf/Booking/Reservation.aspx')
    time.sleep(1)
    
    try:                              
        # 다음달 달력으로 넘기기
        driver.find_element(By.XPATH, f'/html/body/form/div[4]/div[2]/div/div[1]/div[1]/div[1]/div/table/thead/tr[1]/th[3]/a').click()
        time.sleep(1)
        #지정 날짜 클릭하기.                           //*[@id="contents_UpdPandel"]/div[1]/div[1]/div/table/tbody/tr[2]/td[2]/a #세로(주차) #가로(요일)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'/html/body/form/div[4]/div[2]/div/div[1]/div[1]/div[1]/div/table/tbody/tr[{weekVal}]/td[{dayVal}]/a'))
        )
        driver.find_element(By.XPATH, f'//*[@id="contents_UpdPandel"]/div[1]/div[1]/div/table/tbody/tr[{weekVal}]/td[{dayVal}]/a').click()
        time.sleep(1)
        #지정한 날짜의 티를 선택하기 
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"/html/body/form/div[4]/div[2]/div/div[1]/div[1]/div[2]/div/div/div[{courseVal}]/div/table/tbody/tr[{teeVal}]/td[{buVal}]/a/p"))
        )        
        driver.find_element(By.XPATH, f'/html/body/form/div[4]/div[2]/div/div[1]/div[1]/div[2]/div/div/div[{courseVal}]/div/table/tbody/tr[{teeVal}]/td[{buVal}]/a/p').click()
        time.sleep(1)

         #ID1 예약하기
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.ID, 'contents_hypLnkRsvConfrim')))
        elem_btn = driver.find_element(By.ID, 'contents_hypLnkRsvConfrim')
        elem_btn.click() # 예약하기 버튼 클릭

        #예약하기 최종 OK!
        elem_btn = driver.find_element(By.ID, 'contents_lnkBtnReserveOk')
        #elem_btn.click()  #예약완료 버튼
        #print(f"{id} 1번 예약 완료~") 
    except TimeoutException:
        print("시간 초과: 요소를 찾지 못했습니다. 재시도 중...")
        # 재시도 로직 추가 또는 로그 기록 후 종료 처리

   
    while(True):
            pass

# step1.실행 주기 설정
schedule.every(2).seconds.do(access)
#schedule.every().day.at("08:59:58").do(access)

# step2.스캐쥴 시작
while True:
    time.sleep(0.1)
    schedule.run_pending()