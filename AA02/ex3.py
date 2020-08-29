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
    #A nLICÃO DESSE ALGORITMO SE ENCONTRA NO PDF SENOXEX.PDF
    # float x = valor que será usado para calcular e^x
    #truncamento = qual potência será usada para o truncamentp
    if not x > 0 and x <=1:
        print('x deve estar entre (0,1)!')

    else:
        y=0        
        for n in  list(filter(lambda x: x if x%4!=0 else None,range(1,truncamento,1))): #os expoentes utilizados são 1,2,3,5,6,7,9,10,11....
            sinal = (-1) **(n//4) #o sinal das parcelas de sin(x)*e^x seguem um padrão, onde a cada ciclo de 3 numeros,o sinal muda
            cn = 0 #usada para calcular o denominador da parcela
            i = 1
            while i <= n:#itera-se as parcelas de seno(x) (e e(x) indiretamente), começando do i = 1(menor noente do sen(x))
                sinal_parcela = (-1)**(i//2) #calcula-se o sinal da parcela. + para expoentes 1,5,9... e - para expoentes 3,7,11... 
                cn+= sinal_parcela/(math.factorial(i)*math.factorial(n-i)) #esse cálculo se encontra nlicitado no arquivo em senxex.pdf
                i+=2 #i só pode ser ímpar
            #depois de calcular o denominador, o resultado é usado pra calcular sinal*x^n/denominador
            y += sinal*math.pow(x,n)*cn

        return y

if __name__ == "__main__":
    x= 0.5
    truncamento = 9
    real  = (math.e**x)*math.sin(x)
    aprox = senoexponencial(x,truncamento)
    seno = seno(x,truncamento)
    erro_seno = math.sin(x)-seno
    n = exponencial(x,truncamento)
    erro_n = (math.e**x)-n
    erro_estimado = prop_de_erro(seno,erro_seno,n,erro_n,'*')
    erro_real = real-aprox
    print('f(x) = %f'%aprox)
    print('g(x) = %f'%(seno*n))
    print('Erro estimado = %.16f'%erro_estimado)
    print('Erro real = %.16f'%erro_real)
