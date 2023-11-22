import time
import math
import sys
from PyQt5.QtWidgets import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from PyQt5 import uic
from Email import email
from selenium.webdriver.common.by import By
from selenium import webdriver
from PyQt5.QtCore import *
import datetime
class seleniumm(QThread):
    def __init__(self, ID, PW, Max, Min, Search, Plus, Product_set, EmailInfor, Reset, Result):
        super().__init__()
        self.running = True
        self.Can = True
        self.Max = int(Max)
        self.Min = int(Min)
        self.ID = ID
        self.PW = PW
        self.Search = Search
        self.Plus = Plus
        self.Product_set = Product_set #첨에는 빈리스트임 {}
        self.PreviousTrue = False
        self.driver = webdriver.Chrome()
        self.email = email(EmailInfor[0], EmailInfor[1], EmailInfor[2])
        self.Reset = Reset
        self.Result = Result
        print("__________________")
        print(self.Product_set)
        print("__________________")
    def run(self):
        try:
            while self.running:
                count = 0
                self.driver.get(f'https://www.daangn.com/search/{self.Search}')
                self.driver.implicitly_wait(10)
                for i in range(self.Plus):
                    MoreBtn = self.driver.find_element(By.XPATH,'/html/body/section[2]/div[1]/div[2]')
                    actions = ActionChains(self.driver)
                    actions.move_to_element(MoreBtn).perform()
                    MoreBtn.click()
                    time.sleep(1)
                    # self.driver.find_element(By.XPATH,'/html/body/section[2]/div[1]/div[2]').click()
                time.sleep(2)
                Product_list = self.driver.find_elements(By.CLASS_NAME,'flea-market-article')
                print(len(Product_list))
                for i in range(len(Product_list)):
                    try:
                        self.driver.implicitly_wait(10)
                        Product_price_str = self.driver.find_element(By.XPATH,f'//*[@id="flea-market-wrap"]/article[{i+1}]/a/div[2]/p[2]').text
                        price = Product_price_str
                        time.sleep(0.3)
                        if "만원" in Product_price_str:
                            Product_price_str = Product_price_str[:len(Product_price_str)-2] + '0000'
                        else:
                            Product_price_str = Product_price_str[:len(Product_price_str)-1]

                        if Product_price_str == "나눔":
                            continue
                        Product_price = Product_price_str.replace(",","")
                        #가격 필터링 거침
                        if int(Product_price) > self.Max or int(Product_price) < self.Min:
                            continue
                        else:
                            #중복 필터링 거침
                            self.PreviousTrue = True

                            Product_title = self.driver.find_element(By.XPATH, f'// *[ @ id = "flea-market-wrap"] / article[{i+1}] / a / div[1] / img')
                            actions = ActionChains(self.driver)
                            actions.move_to_element(Product_title).perform()
                            time.sleep(0.3)
                            Product_title.click()
                            time.sleep(2)
                            CurrentUrl = self.driver.current_url
                            Product_number = CurrentUrl.split('/')[-1]
                            if Product_number in self.Product_set:
                                self.driver.back()
                                time.sleep(0.3)
                                continue
                            else:
                                body = ""
                                title = self.driver.find_element(By.XPATH,'//*[@id="article-title"]').text
                                body += "가격:" + price + '\n\n'
                                # self.email.send_email()
                                detail = self.driver.find_element(By.ID,'article-detail').text
                                body += "상품내용:\n"
                                body += detail + '\n\n\n'
                                time.sleep(0.5)
                                img = self.driver.find_elements(By.XPATH,
                                                           '/html/body/article/section[1]/div/div/div/div/div/div/div/a/div/div/img')
                                image_src_list = [element.get_attribute("src") for element in img]
                                img_src = ""
                                for src in image_src_list:
                                    if src[::-1][:4] != "gnp.":
                                        img_src = src
                                        break
                                # 이미지 소스 가져오기
                                time.sleep(0.1)
                                body += "대표사진:\n"
                                body += img_src + '\n\n'
                                body += "상품 URL:" + CurrentUrl
                                print(body)
                                print("____________________________-")
                                # print(image_source)
                                self.email.send_email(title, body)
                                count += 1
                                self.Product_set.add(Product_number)
                                self.driver.back()

                    except Exception as e:
                        pass

                time.sleep(1)
                self.PreviousTrue = False
                now = datetime.datetime.now()
                formatted_time = now.strftime("%H:%M:%S")
                self.Result.append("[" + formatted_time +"]   " + f"{count}건 메일 발송 완료\n")
                for i in range(self.Reset):
                    if not self.running:
                        break
                    time.sleep(1)

                print(count)
        except Exception as e:
            print(e)


    def resume(self):
        self.running = True

    def pause(self):
        self.running = False


