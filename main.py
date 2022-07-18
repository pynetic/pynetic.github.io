from pynetic import * 

index = Page(title="Pynetic Test")
header = index.add(Header(
    text="Hello Internet!",
    size=1
))
image = index.add(Image(
    source="[image link]"
))
body = index.add(Paragraph(
    text=[Link([Bold("Pynetic")], "https://github.com/Jabbey92/pynetic"), " aims to be a modern python-based framework for web development"]
))

button = index.add(Button(text="Testing Reactivity!"))
button.set(
    "onclick", reactive.button_click
)

image.set(
    "onclick", reactive.button_click
)

with open("index.html", "w+") as index_x:
    index_x.write(index.render())