import js
from re import compile

class AutoRender:
    def __init__(self, value, callback, stringToFormat, id):
        self.xvalue = value
        self.callback = callback
        self.id = id
        self.stringToFormat = stringToFormat
    
    @property 
    def value(self):
        return self.xvalue
    
    @value.setter
    def value(self, value):
        js.console.log("?")
        self.xvalue = value
        self.callback(value, self.stringToFormat, self.id)

def update(value, stringToFormat, idx):
    x = compile("\{[a-z]+\}")
    x = x.findall(stringToFormat)
    for i in x:
        stringToFormat = stringToFormat.replace(i, "{}")
    js.document.getElementById(idx).innerHTML = stringToFormat.format(value)

x = AutoRender(0, update, "Hello Internet! {x}", "4c077281-77be-4cfe-b1f0-afe35000c82d")

def button_click():
    globals()["x"].value += 1


y = AutoRender(100, update, "Testing Reactivity! {y}", "804ef446-27e1-4fbc-a311-ffd8632a75dc")

def button_click2():
    globals()["y"].value -= 1


