import reactive

class Component:
    def __init__(self):
        self.extra = ""
        self.children = []
        self.tags = {}

    def set(self, key, value):
        self.tags[key] = value.__name__+"()"

    def render(self):
        for key,value in self.tags.items():
            self.extra += f" {key}=\"{value}\""
        tag = self.tag
        children_str = ""
        for child in self.children:
            children_str += str(child)
        return f"<{tag}{self.extra}>{children_str}</{tag}>"

    def __repr__(self):
        return self.render()

class Page(Component):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.tag = "html"
        self.body = []
        self.children = [f"\n\t<head>\n\t\t<title>{title}</title>\n\t\t<link href='/pynetic.css' rel='stylesheet'>\n\t\t<script src=\"https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js\"></script>\n\t</head>\n\t<body>", """<script src="/pynetic.js"></script>"""]

    def render(self):
        body = ""
        i = 0
        for child in self.body:
            body += "\n\t\t"+(str(child).replace("\n", "<br>"))
        self.children.append(body+"\n\t</body>\n")
        for key,value in self.tags.items():
            self.extra += f" {key}=\"{value}\""
        tag = self.tag
        children_str = ""
        for child in self.children:
            children_str += str(child)
        return "<!DOCTYPE HTML>\n"+f"<{tag}{self.extra}>{children_str}</{tag}>"

    def add(self, child):
        self.body.append(child)
        return child

class TextComponent(Component):
    def __init__(self, text):
        super().__init__()
        self.children = text

class Header(TextComponent):
    def __init__(self, text, size=1):
        super().__init__(text)
        self.size = size
        self.tag = "h"+str(size)

class Paragraph(TextComponent):
    def __init__(self, text):
        self.tag = "p"
        super().__init__(text)

class Bold(TextComponent):
    def __init__(self, text):
        self.tag = "b"
        super().__init__(text)

class Image(Component):
    def __init__(self, source):
        super().__init__()
        self.tags = {"src": source}
        self.tag = "img"

class Button(Component):
    def __init__(self, text):
        super().__init__()
        self.children = text
        self.tag = "button"

class Link(TextComponent):
    def __init__(self, text, url):
         super().__init__(text)
         self.url = url
         self.tags = {"href": url}
         self.tag = "a"