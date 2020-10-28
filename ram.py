n = 3
achou = False

def soma(inicio,fim):
    s=0
    for i in range(inicio,fim+1): s+=i
    return s

res = []
for n in range(3,500):
    for casa in range(n//2+1,n):
        
        if soma(1,casa-1)==soma(casa+1,n):
            res.append(n)
        else:
            pass

print(res)

def fun1(k):
    return 1+3