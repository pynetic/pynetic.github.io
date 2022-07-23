from pynetic import * 

index = Page(title="Pynetic Test")
header = index.add(Header(
    text="Hello Internet! {x}",
    size=1
))

body = index.add(Paragraph(
    text=[Link([Bold("Pynetic")], "https://github.com/pynetic"), " aims to be a batteries included python-based framework for web development."]
))

x = 0
button = index.add(Button(text="Testing Reactivity!"))
@header.onclick(bound_to=x, element=button)
def button_click():
    globals()["x"].value += 1

button_click(intialize=True)

y = 100
button2 = index.add(Button(text="Testing Reactivity! {y}"))
@button2.onclick(bound_to=y)
def button_click2():
    globals()["y"].value -= 1

button_click2(intialize=True)

gen_reactive()

with open("index.html", "w+") as indexFile:
    indexFile.write(index.render())