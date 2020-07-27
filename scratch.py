import lxml.html
import urllib.request as urllib2
import pprint
#import http.cookiejar as cookielib
import ssl
from io import BytesIO
from PIL import Image,ImageFilter, ImageEnhance
#import Image
import base64
import pytesseract
import string
import re
import os
import subprocess
import tempfile
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
import mechanize
from mechanize import Browser, Item
#import cookielib

#import cv2


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def form_parsing(html):
   tree = lxml.html.fromstring(html)
   data = {}
   for e in tree.cssselect('.form-horizontal select'):
      print(e)
      if e.get('name'):
         data[e.get('name')] = ''
         for x in e.cssselect('option[selected="selected"]'):
             if x.get('value'):
                data[e.get('name')] = x.get('value')
   return data


def load_captcha(html):
      tree = lxml.html.fromstring(html)
      img_data_all = tree.cssselect('.text-success img')[0].get('src')
      img_data = img_data_all.partition(',')[-1]
      #print(img_data)
      #binary_img_data = img_data.encode('base64').decode('base64');
      base64_img_bytes = img_data.encode('utf-8')
      file_like = BytesIO(base64.decodebytes(base64_img_bytes))
      print(file_like);
      img = Image.open(file_like)
      return img
   #pprint.pprint(tree);
   #return tree
#ckj = cookielib.CookieJar()

def ocr(img):
    # threshold the image to ignore background and keep text
    gray = img.convert('L')
    #gray.save('captcha_greyscale.png')
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    #bw.save('captcha_threshold.png')
    word = pytesseract.image_to_string(bw,config ='--psm 6')
    print(word);
    ascii_word = ''.join(c for c in word if c in string.letters).lower()
    return ascii_word

def autocaptcha(path):
    """Auto identify captcha in path.
    Use pytesseract to identify captcha.
    Args:
        path: string, image path.
    Returns:
        string, OCR identified code.
    """
    im = Image.open(path)

    im = im.convert('L')
    im = ImageEnhance.Contrast(im)
    im = im.enhance(3)
    img2 = Image.new('RGB', (150, 60), (255, 255, 255))
    img2.paste(im.copy(), (25, 10))

    # TODO: add auto environment detect
    return pytesseract.image_to_string(img2)

def capcha():
    img = Image.open('/Users/srinivas/captcha_original.png')
    img_grey = img.convert('L')
    #img_grey.show()
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    img_out = img_grey.point(table, '1')

    text = pytesseract.image_to_string(img_grey)  # 将图片转成字符串
    ###pytesseract验证通过率好像不高，可以试试用百度的
    return text

def imageToStringArray(img):
    t = pytesseract.image_to_string(img, lang='eng', \
                                    config='--oem 3 --psm 12 poe')
    t = t.replace("\n\n", "\n")
    lines = t.split("\n")

    return lines

def imageToStr():
    image = Image.open("/Users/srinivas/captcha_original.png")
    yzm = pytesseract.image_to_string(image)
    yzm = re.sub('[^a-zA-Z0-9]',"",yzm)
    return yzm

def call_tesseract(image_path):
    """
    Calls Tesseract an open source OCR software.
    :param image_path: an image path.
    :return: plain text.
    """
    cnf = '--psm 8'
    result = pytesseract.image_to_string(Image.open(image_path), config=cnf)
    print(result)
    return result.upper().strip().replace(' ', '')[0:9]


def to_text(path):
    tiff_file = tempfile.NamedTemporaryFile(suffix='.tiff')
    FNULL = open(os.devnull, 'w')
    subprocess.call([
        "convert",
        "-density",
        "350",
        path,
        "-depth",
        "8",
        tiff_file.name
    ], stdout=FNULL, stderr=subprocess.STDOUT)

    # TODO: find a way to do this in python?
    # with WandImage(filename=path, resolution=200) as img:
    #     img.compression_quality = 200
    #     img.format='png'
    #     img.save(filename=tempfile)

    extracted_str = pytesseract.image_to_string(Image.open(tiff_file))
    tiff_file.close()
    return extracted_str


def detectText(fileName):
    ocrResult = pytesseract.image_to_string(Image.open(fileName), lang=None,  config='--psm 7')

    return ocrResult

browser = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx))
#browser = urllib2.build_opener(urllib2.HTTPCookieProcessor(ckj))
html = browser.open(
   'https://anyror.gujarat.gov.in/LandRecordRural.aspx'
).read()
#pprint.pprint(html)
form = form_parsing(html)
pprint.pprint(form)
img = load_captcha(html)
img.save('/Users/srinivas/captcha_original.jpg')
gray = img.convert('L')
gray.save('/Users/srinivas/captcha_gray.png')
bw = gray.point(lambda x:0 if x<1 else 255,'1')
bw.save('/Users/srinivas/captcha_thresholded.png')
#im = Image.open("/Users/srinivas/captcha_original.jpg")
#im = im.filter(ImageFilter.CONTOUR)
#im = im.filter(ImageFilter.DETAIL)
#enhancer = ImageEnhance.Contrast(im)
#im = enhancer.enhance(4)
#im = im.convert('L')
#im.save('/Users/srinivas/temp10.png')
#text = pytesseract.image_to_string(Image.open('/Users/srinivas/temp10.png'),lang='eng', config='--psm 2  -c tessedit_char_whitelist=0123456789')
#print(text)
api_key = '2185e868621ade12dbec20ecb4ce282f'
captcha_fp = open('/Users/srinivas/captcha_gray.png', 'rb')
client = AnticaptchaClient(api_key)
task = ImageToTextTask(captcha_fp)
job = client.createTask(task)
job.join()
print(job.get_captcha_text())

ssl._create_default_https_context = ssl._create_unverified_context
br = Browser()
#cj = cookielib.LWPCookieJar()
#br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_debug_http(True)
br.set_debug_responses(True)
br.set_debug_redirects(True)

br.set_handle_refresh(mechanize._https.HTTPRefreshProcessor(), max_time=1)
hh = mechanize.HTTPSHandler()  # you might want HTTPSHandler, too
hh.set_httpS_debuglevel(1)
br.set_handle_robots(False)
br.open('https://anyror.gujarat.gov.in/LandRecordRural.aspx')

def select_form(form):
  return form.attrs.get('id', None) == 'form1'

br.select_form(predicate=select_form)
br.form.set_all_readonly(False)

for control in br.form.controls:
    print(control)
    if control.type == "select":  # means it's class ClientForm.SelectControl
        for item in control.items:
            print(" name=%s values=%s" % (item.name, str([label.text for label in item.get_labels()])))

br.form['ctl00$ContentPlaceHolder1$drpLandRecord']=['6']
br.form['ctl00$ContentPlaceHolder1$ddlDistrict']=['18']

item = Item(br.form.find_control(name='ctl00$ContentPlaceHolder1$ddlTaluka'),
           {'contents': '4', 'value': '4', 'label': 4})
br.form['ctl00$ContentPlaceHolder1$ddlTaluka']=['4']

item1 = Item(br.form.find_control(name='ctl00$ContentPlaceHolder1$ddlVillage'),
           {'contents': '003', 'value': '003', 'label': '003'})
br.form['ctl00$ContentPlaceHolder1$ddlVillage']=['003']

br.form.new_control('select', 'ctl00$ContentPlaceHolder1$ddlSurveyNo',{'__select' : {'name': 'ctl00$ContentPlaceHolder1$ddlSurveyNo', 'id': 'ctl00$ContentPlaceHolder1$ddlSurveyNo', 'class': 'form-control'} })
br.form.fixup()

item2 = Item(br.form.find_control(name='ctl00$ContentPlaceHolder1$ddlSurveyNo'),
           {'contents': '172', 'value': '172', 'label': 172})
br.form['ctl00$ContentPlaceHolder1$ddlSurveyNo']=['172']

br.form['ctl00$ContentPlaceHolder1$txt_captcha_1'] = job.get_captcha_text()

response = br.submit(id='ContentPlaceHolder1_btnGo')
print(response.read())
print(response.geturl()) # URL of the page we just opened
print(response.info())   # headers
br.back()   # go back

#img = cv2.imread('/Users/srinivas/captcha_original.png')
#custom_config = r'--oem 3 --psm 6'
#text= pytesseract.image_to_string(img, config=custom_config)
#print(text)
#pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
#custom_oem_psm_config = r'--oem 3 --psm 8'
#text = pytesseract.image_to_string(Image.open('/Users/srinivas/captcha_gray.png'),lang='eng', config='--psm 8  -c tessedit_char_whitelist=0123456789')
#text = detectText('/Users/srinivas/captcha_gray.png')
#pprint.pprint(text)

#with open('/Users/srinivas/decoded_image.png', 'wb') as file_to_save:
 #   decoded_image_data = base64.decodebytes(base64_img_bytes)
  #  file_to_save.write(decoded_image_data)
#img.save('/Users/srinivas/captcha_original.png')
#gray = img.convert('L')
#gray.save('/Users/srinivas/captcha_gray.png')
#bw = gray.point(lambda x:0 if x<1 else 255,'1')
#bw.save('/Users/srinivas/captcha_thresholded.png')
#pytesseract.image_to_string(bw)
#pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'
#img1=Image.open('/Users/srinivas/captcha_thresholded.png')
#pytesseract.image_to_string(img1)
#pprint.pprint(word);

#word = pytesseract.image_to_string(bw)
#ascii_word = ''.join(c for c in word if c in string.letters).lower()
#pprint.pprint(ascii_word)



