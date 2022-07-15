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

def setTemplate(color='255, 255, 255', highlightColor="255, 255, 0", font="Heavitas.ttf", fontsize=55):
    """
    Sets the template for the text.

    Parameters
    ----------
    color : str
        The default color of the text in RGB
        Example: '255, 255, 255'
    highlightColor : str
        The highlight of the text when you use <kw>. Default at yellow
    font : str
        The font of the text.
    fontsize : int
        The size of the text.
    """
    with open("textGenerate.html","r") as tf:
        template = tf.read()
    

    url = os.path.abspath(font).replace('\\','/')
    newTemplateSettings = [
        ("FONT_SIZE", str(fontsize)),
        ("COLOR_HERE", str(highlightColor)),
        ("DEFAULT_COLOR", str(color)),
        ("URL_HERE", f"'{url}'")
    ]
    
    for s in newTemplateSettings:
        template = template.replace(s[0], s[1])

    with open("temp.html", "w+") as f:
        f.write(template)
    url = "file://"+os.path.abspath("temp.html")
    if driver.current_url == url:
        driver.refresh()
    else:
        driver.get(url)
    
    driver.execute_script('document.body.style.MozTransform = "scale(3)";')
    driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

def text(text, resolution=(1280,720), transparent=True):
    """
    Generates an image of the text.

    Parameters
    ----------
    text : str
        The text to be rendered.
    resolution : tuple
        The resolution of the image.
    transparent : bool
        Whether the image should be transparent.

    Returns
    -------
    Image
        The image of the text.
    """
    task_id = str(uuid_lib.uuid4())
    turn.append(task_id)

    while turn[0] != task_id:
        time.sleep(0.1)
    
    driver.execute_script("document.getElementById('textElement').innerHTML = arguments[0];", text)
    fileName = str(uuid_lib.uuid4())+".png"
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