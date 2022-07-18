from pynetic import * 

index = Page(title="Pynetic Test")
header = index.add(Header(
    text="Hello Internet!",
    size=1
))

body = index.add(Paragraph(
    text=[Link([Bold("Pynetic")], "https://github.com/pynetic"), " aims to be a batteries included python-based framework for web development."]
))

button = index.add(Button(text="Testing Reactivity!"))
button.set(
    "onclick", reactive.button_click
)

with open("index.html", "w+") as index_x:
    index_x.write(index.render())