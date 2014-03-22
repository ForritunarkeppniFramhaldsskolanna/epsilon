

words = open("/home/suprdewd/misc/Data/Icelandic/Dictionary.txt", "r", encoding='latin1').read().strip().split('\n')

for w in words:
    if all( ord('a') <= ord(c) <= ord('z') for c in w ) and all( a < b for a, b in zip(w, w[1:]) ):
        print(w)





