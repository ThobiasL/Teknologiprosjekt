from pyflowchart import Flowchart
with open("your_file.py") as f:
    code = f.read()

fc = Flowchart.from_code(code)
print(fc.flowchart())
