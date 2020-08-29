from ex1 import exponencial
from ex2 import seno
import math

def prop_de_erro(x1,errox1,x2,errox2,op):
    #de acordo com a literatura, para cada operação entre 2 números têm-se a seguinte propagaçao de erro
    if op == '+':
        erro = errox1+errox2
    elif op == '-':
        erro = errox1-errox2
    elif op == '*':
        erro = x1*errox2 + x2*errox1
    elif op == '/':
        erro = (x2*errox1 - x1*errox2)/(x2**2)

    return erro

def senoexponencial(x,truncamento):
    #A EXPLICÃO DESSE ALGORITMO SE ENCONTRA NO PDF SENOXEX.PDF
    # float x = valor que será usado para calcular e^x
    #truncamento = qual potência será usada para o truncamentp
    if not x > 0 and x <=1:
        print('x deve estar entre (0,1)!')

    else:
        y=0        
        for exp in  list(filter(lambda x: x if x%4!=0 else None,range(1,truncamento,1))): #os expoentes utilizados são 1,2,3,5,6,7,9,10,11....
            sinal = (-1) **(exp//4) #o sinal das parcelas de sin(x)*e^x seguem um padrão, onde a cada ciclo de 3 numeros,o sinal muda
            deno = 0 #usada para calcular o denominador da parcela
            n = exp//2 #usada para a iteração
            par = 1- exp%2 #1 se exp é par, 0 se exp é ímpar
            for exp in range((n+1-par)):#itera-se as parcelas de seno(x) (e e(x) indiretamente),por expoente, indo até n-1, se ímpar, e até n
                sinal_parcela = (-1)**exp #calcula-se o sinal da parcela. + para expoentes 
                deno+= sinal_parcela/(math.factorial(2*exp+1)*math.factorial(2*(n-exp)-int(par))) #esse cálculo se encontra explicitado no arquivo em senxex.pdf
            
            y += sinal*math.pow(x,exp)*deno

        return y

if __name__ == "__main__":
    x= 0.5
    truncamento = 9
    real  = (math.e**x)*math.sin(x)
    aprox = senoexponencial(x,truncamento)
    seno = seno(x,truncamento)
    erro_seno = math.sin(x)-seno
    exp = exponencial(x,truncamento)
    erro_exp = (math.e**x)-exp
    erro_estimado = prop_de_erro(seno,erro_seno,exp,erro_exp,'*')
    erro_real = real-aprox
    print('f(x) = %f'%aprox)
    print('g(x) = %f'%(seno*exp))
    print('Erro estimado = %.16f'%erro_estimado)
    print('Erro real = %.16f'%erro_real)
