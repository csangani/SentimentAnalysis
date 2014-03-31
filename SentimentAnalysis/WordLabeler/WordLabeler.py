import codecs

labels = []

def labelSet(s):
    print(s)
    count = 0
    for l in labels:
        print (count, l)
        count = count + 1
    print (len(labels), 'other')
    val = -1
    label = ''
    flag = True
    while flag:
        try:
            val = int(input('Choose: '))
            if val < len(labels) + 1 and val > -1:
                if val == len(labels):
                    label = input('Specify: ')
                    labels.append(label)
                else:
                    label = labels[val]
                flag = False
        except:
            return
    output = codecs.open('../Data/Labels.txt', 'a+', encoding='utf-8-sig')
    output.write(s + ' : ' + label + '\r\n')
    output.close()

if __name__ == '__main__':

    f = codecs.open('../Data/Synsets.txt', 'r', encoding='utf-8-sig')
    for s in f.readlines():
        try:
            labelSet(s.strip())
        except KeyboardInterrupt:
            pass
    
    f.close()
    output.close()