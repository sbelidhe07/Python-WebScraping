from selenium import webdriver
from PIL import Image
import time
from selenium.webdriver.support.ui import Select
import base64
from io import BytesIO
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import os
import uuid
#from translate import Translator

class LandDetails:
    def __init__(self):
        time.sleep(2)

    def getlandrecordinfo(self,landrecord,district,taluka,village,surveyno):
        custom_options = webdriver.ChromeOptions()
        prefs = {
            "translate_whitelists": {"gu": "en"},
            "translate": {"enabled": "true"}
        }
        custom_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome('/Users/srinivas/Downloads/chromedriver',chrome_options=custom_options)
        #driver = webdriver.Chrome('/Users/srinivas/Downloads/chromedriver')
        driver.get('https://anyror.gujarat.gov.in/LandRecordRural.aspx')

        select1 = Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$drpLandRecord"))
        select1.select_by_value(landrecord)

        select2 = Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlDistrict"))
        select2.select_by_value(district)
        time.sleep(2)

        select3 = Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlTaluka"))
        select3.select_by_value(taluka)
        time.sleep(2)

        select4 = Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlVillage"))
        select4.select_by_value(village)
        time.sleep(2)

        select5 = Select(driver.find_element_by_name("ctl00$ContentPlaceHolder1$ddlSurveyNo"))
        select5.select_by_value(surveyno)

        image_element = driver.find_element_by_xpath("//img[@id='ContentPlaceHolder1_i_captcha_1']")
        img_data_all = image_element.get_attribute("src")
        img_data = img_data_all.partition(',')[-1]
        base64_img_bytes = img_data.encode('utf-8')
        file_like = BytesIO(base64.decodebytes(base64_img_bytes))
        img = Image.open(file_like)

        img.save('/Users/srinivas/captcha_original.jpg')
        gray = img.convert('L')
        gray.save('/Users/srinivas/captcha_gray.png')
        image = Image.open('/Users/srinivas/captcha_original.jpg')

        api_key = '2185e868621ade12dbec20ecb4ce282f'
        captcha_fp = open('/Users/srinivas/captcha_gray.png', 'rb')
        client = AnticaptchaClient(api_key)
        task = ImageToTextTask(captcha_fp)
        job = client.createTask(task)
        job.join()

        txtbox1 = driver.find_element_by_id('ContentPlaceHolder1_txt_captcha_1')
        txtbox1.send_keys(job.get_captcha_text())
        time.sleep(3)

        driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnGo').click()
        time.sleep(3)
        content=driver.page_source.encode('utf-8')
        path = r"/Users/srinivas"
        filename = "%s_page_grab.htm" % uuid.uuid4()
        #translator = Translator(from_lang="gujarati", to_lang="english")
        with open(os.path.join(path, filename), 'wb') as f:
            #translation = translator.translate(content.decode('utf-8'))
            f.write(content)
        driver.quit()
        custom_options = webdriver.ChromeOptions()
        prefs = {
            "translate_whitelists": {"gu": "en"},
            "translate": {"enabled": "true"}
        }
        custom_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome('/Users/srinivas/Downloads/chromedriver', chrome_options=custom_options)
        time.sleep(3)
        # driver = webdriver.Chrome('/Users/srinivas/Downloads/chromedriver')
        #driver.get('https://anyror.gujarat.gov.in/LandRecordRural.aspx')
        driver.get("file://" + os.path.join(path, filename))
        #time.sleep(3)

        #lbl = driver.find_element_by_xpath("//span[@id='ContentPlaceHolder1_lblDistrict']")
        #translator = Translator(from_lang="gujarati", to_lang="english")
        #translation = translator.translate(content)
        #time.sleep(2)
        #print(translation)
        #print(repr(content))
        return "Done"


if __name__ == '__main__':
	h = LandDetails()
	h.getlandrecordinfo('1','18','04','003','172')
