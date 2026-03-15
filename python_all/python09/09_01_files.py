# Use open function to read the content of a file!
# f = open('sampel.txt', 'r')
f = open('sampel.txt') # by default the mode is r
# data = f.read()
data = f.read(5)   # reads first 5 characters from the file
print(data)
f.close()
