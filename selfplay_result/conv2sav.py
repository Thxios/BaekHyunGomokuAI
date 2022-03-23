

base = 'raw/'
save = 'sav/'
for i in range(11):

    target = '1000_2000_%d.txt' % i

    with open(base + target, 'r') as f:
        lines = f.readlines()[:-1]


    with open(save + target[:-4] + '.sav', 'w') as f:
        f.write('15\n15\n%d\n' % len(lines))
        for line in lines:
            x, y = eval(line.rstrip())
            f.write('%d %d\n' % (y, x))

