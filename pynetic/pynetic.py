from uuid import uuid4 as gen_uuid
from functools import wraps 
from inspect import getsource
from re import compile
from time import time

start = time()

reactive = ["""import js\nfrom re import compile\n\nclass AutoRender:\n    def __init__(self, value, callback, stringToFormat, id):\n        self.xvalue = value\n        self.callback = callback\n        self.id = id\n        self.stringToFormat = stringToFormat\n    \n    @property \n    def value(self):\n        return self.xvalue\n    \n    @value.setter\n    def value(self, value):\n        js.console.log("?")\n        self.xvalue = value\n        self.callback(value, self.stringToFormat, self.id)\n\ndef update(value, stringToFormat, idx):\n    x = compile("\\{[a-z]+\\}")\n    x = x.findall(stringToFormat)\n    for i in x:\n        stringToFormat = stringToFormat.replace(i, "{}")\n    js.document.getElementById(idx).innerHTML = stringToFormat.format(value)\n\n"""]
class AutoRender:
    def __init__(self, value, callback):
        self.xvalue = value
        self.callback = callback
    
    @property 
    def value(self):
        return self.xvalue
    
    def __repr__(self):
        return self.xvalue

    @value.setter
    def value(self, value):
        self.xvalue = value
        self.callback(value)

def gen_reactive():
    with open("reactive.py", "w+") as reactiveFile:
        reactiveFile.write("".join(reactive))

class Component:
    def __init__(self):
        self.extra = ""
        self.children = []
        self.uuid = gen_uuid()
        self.tags = {"id": self.uuid}

    def set(self, key, value):
        self.tags[key] = value.__name__+"()"

    def onclick(self, bound_to, element=None):
        def decorator_onclick(func):
            @wraps(func)
            def wrapper_onclick(*args, **kwargs):
                self.bound_to = bound_to
                if "intialize" not in list(kwargs.keys()):
                    func(*args, **kwargs)

                if element != None:
                    element.set("onclick", func)
                else:
                    self.set("onclick", func)

                # ASSUMES self.text **IS** a string, **NOT** a list
                x = compile("{[a-z]+}")
                varname = x.search(self.children)[0][1:-1]
                reactive.append(f"""{varname} = AutoRender({bound_to}, update, "{self.children}", "{self.uuid}")\n\n""")
                reactive.append("\n".join(getsource(func).split("\n")[1:])+"\n\n")
            return wrapper_onclick
        return decorator_onclick

    def render(self):
        for key,value in self.tags.items():
            self.extra += f" {key}=\"{value}\""
        tag = self.tag
        children_str = ""
        for child in self.children:
            children_str += str(child)

        if children_str.__contains__("{") and children_str.__contains__("}"):
            z = compile("{[a-z]+}")
            z = z.findall(children_str)
            for i in z:
                children_str = children_str.replace(i, "{}")
            children_str = children_str.format(self.bound_to)

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
        end = time()
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
        
    

        print(f"Finished in {round((end-start)*1000, 3)} ms")
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