import math 
# e^x = sum(x^n/n!), 0<n<inf
def exponencial(x,truncamento):
    # float x = valor que será usado para calcular e^x
    #truncamento = qual potência será usada para o truncamentp
    if not x > 0 and x <=1: 
        print('x deve estar entre (0,1)!')
    else:
        y=0        
        for exp in range(truncamento): #truncar na potencia anterior a do truncamento, ou seja, de [0,truncamento-1]
            y += math.pow(x,exp)/math.factorial(exp) #soma-se a parcela x^exp/exp!

        return y
        
if __name__ == "__main__":
    x = 0.5
    aprox = exponencial(x,9) #valor de e^x pela série de mclaurin
    real = math.e**x #valor real de e^x
    print("Exponencial de %f = %f "%(x,aprox))
    print("Erro absoluto = %.16f"%(real-aprox))
