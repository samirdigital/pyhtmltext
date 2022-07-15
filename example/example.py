import pyhtmltext

pyhtmltext.setTemplate(
    color = "255, 255, 255", # White text,
    highlightColor = "255, 255, 0", # Yellow <kw>'s 
    fontsize = 200
)

img = pyhtmltext.text("Test")
img.save("test.png")