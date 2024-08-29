x=10

def blah():
    global x
    print("Blah : ",x)
    x = 20
print("Initially , x = ",x)
blah()
print("Post-blah, x = ",x)