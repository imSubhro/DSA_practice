f = open('poems.txt')
t = f.read()
if 'twinkle' in t:
    print("Twinkle is preasent")
else:
    print("Twinkle is not preasent")
    f.close()