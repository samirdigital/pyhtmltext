# pyhtmltext
Generate text in Python from an HTML page, allowing for things like highlighting or changing the color of a specific word a lot easier.

# Installation
``pip3 install -r requirements.txt``

# Usage:
```python
import pyhtmltext

pyhtmltext.setTemplate(
    color = "(255, 255, 255)", # White text,
    highlightColor = "(255, 255, 0)", # Yellow <kw>'s 
    font = "Heavitas.ttf",
    fontsize = 50
)

img = pyhtmltext.text("Test")
```