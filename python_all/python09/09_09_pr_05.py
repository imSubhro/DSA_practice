words = ["donkey", "kaddu", "mote"]

with open("sampel.txt") as f:
    content = f.read()

 
for word in words:
  content = content.replace(word, "$%^@$^#")


with open("sampel.txt", "w") as f:
  f.write(content)
  