from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse 
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from googletrans import Translator

@csrf_exempt
def index(request):
    masuk=request.POST['masook']
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="E:\chromedriver.exe",options=chrome_options)
    fetch = "https://jisho.org/search/" + masuk+'%20%23kanji'
    driver.get(fetch)
    meaning=driver.find_element_by_class_name("kanji-details__main-meanings")
    try:
        onyomi=driver.find_element_by_xpath("""//*[@id="result_area"]/div/div[1]/div[2]/div/div[1]/div[2]/dl[1]""")
        onyomi=str(onyomi.text)[4:].split('、')
    except common.exceptions.NoSuchElementException as identifier:
        onyomi=None
    try:
        kunyomi=driver.find_element_by_xpath("""//*[@id="result_area"]/div/div[1]/div[2]/div/div[1]/div[2]/dl[2]""")
        kunyomi=str(kunyomi.text)[4:].split('、')
    except common.exceptions.NoSuchElementException as identifier:
        kunyomi=None
    jlpt=driver.find_element_by_xpath("""//*[@id="result_area"]/div/div[1]/div[2]/div/div[2]/div/div[2]""")
    jlpt=str(jlpt.text).strip()
    
    translator= Translator()
    arti=translator.translate(meaning.text,src='en',dest='id')
    responseData = {
        'artinya': str(arti.text),
        'onyominya': onyomi,
        'kunyominya' : kunyomi,
        'jlptnya' : jlpt
    }
    return JsonResponse(responseData)