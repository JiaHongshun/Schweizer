

def givepath():
    import os
    a = os.path.split(os.path.realpath(__file__))
    print(a[0])

if __name__ == "__main__":
    givepath()
