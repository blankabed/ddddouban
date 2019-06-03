import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import re
from bs4 import BeautifulSoup
from urllib import request
from 学校爬虫 import YDMHTTP


browser=webdriver.Chrome(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
wait=WebDriverWait(browser, 10)

def get_url(url):
    browser.get(url)
    input=browser.find_element_by_css_selector("#J-userName")
    input.send_keys("15215966137")
    pwd=browser.find_element_by_css_selector("#J-password")
    pwd.send_keys("!980723sqk")
    img=browser.find_element_by_css_selector("#J-loginImg")
    src=img.get_attribute('src')
    request.urlretrieve(src,'./img_1.png')
    from YDMHTTP import decode
    result = decode('img_1.png', 6701)
    print('选项', result)  # 返回的是字符串

    # 根据识别结果点击图片
    position_list = [(40, 70), (110, 70), (180, 70), (252, 70), (40, 150), (110, 150), (180, 150), (250, 150)]
    if result != '看不清':
        for position in result:
            ActionChains(window).move_to_element_with_offset(img_ele, position_list[int(position) - 1][0],
                                                             position_list[int(position) - 1][1]).click().perform()

    # 点击登录按钮
    login_button = window.find_element_by_id('J-login')
    login_button.click()


def main():
    url="https://kyfw.12306.cn/otn/resources/login.html"
    get_url(url)
