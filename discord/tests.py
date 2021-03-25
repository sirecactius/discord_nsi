a = '000Ryujin42¤motdepasse'

print(a[:3])
a = a[3:]
for i in range(len(a)):
    if a[i] == '¤':
        print(a[:i])
        print(a[i+1:])
