from ex1 import exponencial
from ex2 import seno
import math

def prop_de_erro(x1,errox1,x2,errox2):
    erro = abs(x1*errox2) + abs(x2*errox1)

    return erro

"""def senoexponencial(x,truncamento):
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
"""

if __name__ == "__main__":
    x= 0.5
    truncamento = 9
    seno = seno(x,truncamento)
    erro_seno = abs(math.sin(x)-seno)
    exp = exponencial(x,truncamento)
    erro_exp = abs((math.e**x)-exp)
    estimado = seno*exp
    erro_estimado = prop_de_erro(seno,erro_seno,exp,erro_exp)
    real  = (math.e**x)*math.sin(x)
    erro_real = abs(real-estimado)

    print('seno(x) = %.16f'%seno)
    print('exponencial(x) = %.16f'%exp)
    print('f(x) = %.16f'%(estimado))
    print('g(x) = %.16f'%(real))
    print('Erro estimado = %.16f'%erro_estimado)
    print('Erro real = %.16f'%erro_real)
    print('Diferença entre erros = %.16f'%(abs(erro_real-erro_estimado)))

"""f(x) = exp(x)*sin(x)
erro_f = abs(df/dexp * erro_exp)+abs(df/dsin * erro_seno)

erro_f = modulo(df/dx * erro_x) + modulo(df/dy * erro_y)

f(exp(x),sin(x)) = exp(x)*sin(x)
f(x) = c*x
df/dx = c
df/dexp = sin(x)
df/dsin = exp(x)

f(exp(x),sin(x)) = exp(x) + sin(x)
df/dexp = 
f(x,y) = x + y
f(x) = x + c
df/dx = 1
f(y) = y + c
df/dy = 1
erro_f = modulo(1*erro_x) + modulo(1*erro_y) 

f(x,y) = x - y
df/x = 1
df/dy = -1
erro_f = modulo(erro_x) + modulo(-1*ero_y)

f(x,y) = x*y
f(x) = c*x
df/dx = c
f(y) = c*y
df/dy = c
erro_f = modulo(y*erro_x) + modulo(x*erro_y)

f(x,y) = x/y
f(x) = x/c
df/dx = 1/c
f(y) = y/c
df/dy = 1/c
erro_f = modulo(1/y * erro_x) + modulo(1/x) * erro_y)

"""