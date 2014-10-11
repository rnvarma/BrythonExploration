def rohanRocks():
    for i in xrange(10):
        kosbie = 0
        while( i >= 0):
            for y in xrange(i):
                kosbie += 1
            i -= 1
        print kosbie,


# rohanRocks()


def soDoesRudina(x):
    for i in xrange(x, -x, -2):
        if (i < 0): step = -1
        else: step = 1
        print "#", i, ":",
        for j in xrange(-i, i, step):
            if i * j > 0:
                print (i, j),
        print

soDoesRudina(5)