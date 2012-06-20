import sys
import os
import operator


fin = file(sys.argv[1])
froute = file(sys.argv[2],'w')
finter = file(sys.argv[3],'w')

cnt = 0
for line in fin.readlines():
    cnt +=1
    pair = ';'.join(line.split()[0:2])
    froute.write(str(cnt)+' '+pair+'\n')
    finter.write(str(cnt)+' 10'+'\n')

froute.close()
finter.close()
fin.close()

