import math 
# e^x = sum(x^n/n!), 0<n<inf
def exponencial(x,truncamento):
    # float x = valor que será usado para calcular e^x
    #truncamento = qual potência será usada para o truncamentp
    if not x > 0 and x <=1: 
        print('x deve estar entre (0,1)!')
    else:
        y=0        
        for exp in range(truncamento+1): #truncar na potencia anterior a do truncamento, ou seja, de [0,truncamento-1]
            y += x**exp/math.factorial(exp) #soma-se a parcela x^exp/exp!

        return y
        

"""e^x = 1+x+x2/2+x3/6+x4/24......"""
"""sin(x) = 1*x+1*x3/6
if __name__ == "__main__":
    x = 0.5 #0<x<1
    real = math.e**x #valor real de e^x
    aprox = exponencial(x,9) #valor de e^x pela série de mclaurin
    print("Valor real = %.16f"%real)
    print("Exponencial de %f = %.16f "%(x,aprox))
    print("Erro absoluto = %.16f"%(real-aprox))
"""