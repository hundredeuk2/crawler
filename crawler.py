import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from tqdm.auto import tqdm

import time
from bs4 import BeautifulSoup
import requests

import argparse
from omegaconf import OmegaConf
from counting import cal

from pyvirtualdisplay import Display

def main(config):

    # display = Display(visible = 0, size = (1024, 768))
    # display.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    # chrome_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"')
    chrome_options.add_argument("lang=ko_KR")


    service = Service("./chromedriver")    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")

    # driver = webdriver.Chrome(service='./chromedriver', options=chrome_options)

    URL = config.url
    driver.get(URL)

    app_name = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1').text
    num = driver.find_element(By.CLASS_NAME, 'EHUI5b').text.split(' ')[1][:-1]
    num = cal(num)
    if num > 600 :
        num = 600 


    # 리뷰 클릭 후 스크롤
    driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/header/div/div[2]/button/i')[0].click()

    # 스크롤이 동작하지 않는 경우에만 선택적으로 적용합니다.
    # 크롬창을 최대화합니다.
    driver.maximize_window()

    scroll_count = num

    review_div = driver.find_element(By.CLASS_NAME, "fysCi")
    time.sleep(1)
    for i in tqdm(range(scroll_count)):
        driver.execute_script("arguments[0].scrollTo(0, document.body.scrollHeight+999999999999)", review_div)
        time.sleep(1)

    # 스크롤을 다시 맨 위로 이동
    driver.execute_script('arguments[0].scrollTo(0, 0);', review_div)

    review_box_list = driver.find_elements(By.CLASS_NAME, "RHo1pe")
    print("> 리뷰개수 :", len(review_box_list))


    f = open(f"{app_name}.txt", "w", encoding = "utf-8")

    for review_box in tqdm(review_box_list):
        # 별점
        review_star = review_box.find_element(By.CLASS_NAME, "iXRFPc")
        user_text = review_box.find_element(By.CLASS_NAME, "X5PpBb").text        
        star_label = review_star.get_attribute("aria-label")[10]
        # 작성일자
        review_date = review_box.find_element(By.CLASS_NAME, "bp9Aid").text
        # 리뷰 텍스트
        review_text = review_box.find_element(By.CLASS_NAME, "h3YV2d").text
        # 파일에 기록하기 + 출력하기
        f.write(review_date + "\t" + star_label + "\t" + user_text 
                +"\t" +review_text + "\n")
        #print(review_date + "\t" + star_label + "\t" + review_text)
    f.close()
    driver.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='example')
    args, _ = parser.parse_known_args()
    ## python --config yamlfile.yaml

    config = OmegaConf.load(f'./configs/{args.config}.yaml')
    main(config)