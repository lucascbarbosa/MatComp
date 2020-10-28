import math
def seno(x,truncamento):
    # float x = valor que será usado para calcular e^x
    #truncamento = qual potência será usada para o truncamentp
    if not x > 0 and x <=1:
        print('x deve estar entre (0,1)!')

    else:
        y=0        
        print()
        for k in range(int(((truncamento-1)/2)+1)): #truncar na potencia anterior a do truncamento, ou seja, de [0,truncamento-1]
            sinal = (-1)**k #calcula-se o sinal da parcela: +1 para os expoentes 1,5,9.... e -1 para os expoentes 3,7,11...
            y += sinal*math.pow(x,1+2*k)/math.factorial(1+2*k) #soma-se a parcela sinal*x^exp/exp!

        return y

if __name__ == "__main__":

    x = math.pi/6 #qqr x 0<x<1
    real = math.sin(x) #valor real calculado pela biblioteca
    aprox = seno(x,9) #valor aproximado pela série de maclaurin
    print("Seno real de %f = %.16f"%(x,real))
    print("Seno de %f = %.16f"%(x,aprox))
    print("Erro absoluto = %.16f"%(abs(real-aprox)))
