# Uses Selenium & HTML to generate text

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import uuid as uuid_lib
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.maximize_window()
turn = []

def setTemplate(color, fontsize=55):
    with open("assets/textGenerate.html","r") as tf:
        template = tf.read()
    template = template.replace("FONT_SIZE", str(fontsize)).replace("COLOR_HERE", str(color))
    with open("temp/temp.html", "w+") as f:
        f.write(template)
    url = "file://"+os.path.abspath("temp/temp.html")
    if driver.current_url == url:
        driver.refresh()
    else:
        driver.get(url)
    
    driver.execute_script('document.body.style.MozTransform = "scale(3)";')
    driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

def text(text, resolution=(1280,720), transparent=True):
    task_id = str(uuid_lib.uuid4())
    turn.append(task_id)

    while turn[0] != task_id:
        time.sleep(0.1)
    
    driver.execute_script("document.getElementById('textElement').innerHTML = arguments[0];", text)
    fileName = 'temp/' + str(uuid_lib.uuid4())+".png"
    time.sleep(0.1)
    driver.implicitly_wait(5)
    driver.find_element(By.ID, "textElement").screenshot(fileName)
    turn.remove(task_id)

    im = Image.open(fileName)
    if transparent:
        pix = im.load()
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                # if the average of the red and blue values is less than 40% of the green value,
                if pix[x,y][1] != 0 and (((pix[x,y][0]+pix[x,y][2])/2) / (pix[x,y][1])) < 0.4:
                    pix[x,y] = (0,0,0,0)

    final_image = Image.new('RGBA', resolution, (0,0,0,0) if transparent else (0, 255, 0, 255))
    im = im.resize((int(im.size[0]/2), int(im.size[1]/2)))
    final_image.paste(im, (int((resolution[0]-im.size[0])/2), int((resolution[1]-im.size[1])/2)))
    
    im.close()
    os.remove(fileName)
    return final_image