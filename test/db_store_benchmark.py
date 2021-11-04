###########
# dbm
###########
#%%
import re
import dbm
from time import time

db = dbm.open('test.db', flag='n')
db['我們'] = str(1)
db['我a'] = str(2)
db.sync()
db.close()

db = dbm.open('test.db', flag='r')
pat_ch_chr = re.compile("[〇一-\u9fff㐀-\u4dbf豈-\ufaff]")

for k in db:
    k = k.decode('utf-8')
    if any(not pat_ch_chr.search(ch) for ch in k):
        print('matched:', k, int(db[k]))
    print()

# db.close()
#%%

mydict = dbm.open('myfile2.db', flag='n')

s = time()
for i in list(range(5000))*3:
    i = str(i)
    if i not in mydict:
        mydict[i] = str(1)
    else:
        mydict[i] = str(int(mydict[i]) + 1)
mydict.sync()
e = time()
print(e-s)
mydict.close()
# Write time: 1.4570286273956299 sec

#%%
mydict = dbm.open('myfile2.db', flag='r')

results = []
s = time()
for i in list(range(5000))*3:
    results.append(int(mydict[str(i)]))
e = time() - s
print(e)
mydict.close()
# Read time: 0.37085318565 sec


###################
# dbdict
##################
#%%
from dcctk.dbdict import dbdict
from time import time

db = dbdict('test.sqlite')


s = time()
for i in list(range(10000)):
    if i not in db:
        db[i] = 1
    else:
        db[i] = db[i] + 1
e = time()
print(e - s)
db.close()
# Write time: 

###################
## SqliteDict
###################
#%%
from time import time
from sqlitedict import SqliteDict

mydict = SqliteDict('./test.sqlite', flag='n', autocommit=True)

s = time()
for i in list(range(10000)):
    if i not in mydict:
        mydict[i] = 1
    else:
        mydict[i] = mydict[i] + 1
e = time()
print(e - s)
mydict.close()
# Write time: 22.42469811439514 sec

#%%
mydict = SqliteDict('./test.sqlite', flag='n', autocommit=False)

s = time()
for i in list(range(5000))*3:
    if i not in mydict:
        mydict[i] = 1
    else:
        mydict[i] = mydict[i] + 1
mydict.commit()
e = time()
print(e - s)
mydict.close()
# Write time: 14.626226902008057 sec

#%%
results = []
mydict = SqliteDict('./test.sqlite', flag='r')

s = time()
for i in list(range(10000)):
    results.append(i in mydict)
e = time() - s
print(e)
mydict.close()
# Read time: 3.8324692249298096




########### 
# Native dictionary (in-memory) 
# ########
#%%
mdict = {}
s = time()
for i in list(range(10000)):
    if i not in mdict:
        mdict[i] = 1
    else:
        mdict[i] = mdict[i] + 1
e = time()
print(e - s)

#%%
results = []
s = time()
for i in list(range(10000)):
    results.append(4555 in mdict)
e = time()
print(e - s)