import sys

with open("repodoctor/mega.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('f\\"\\"\\"', 'f"""')
c = c.replace('\\"\\"\\"', '"""')

with open("repodoctor/mega.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed syntax error")
