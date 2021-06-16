import random,string
st=''
for j in range(5):  #生成5个随机英文大写字母
    st+=random.choice(string.ascii_uppercase)

print(st)