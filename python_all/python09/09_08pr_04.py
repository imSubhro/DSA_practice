with open("sampel.txt") as f:
    content = f.read()

content = content.replace("donkey", "$%^@$^#")

with open("sampel.txt", "w") as f:
  f.write(content)

