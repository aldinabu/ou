# -*- coding: utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt

def option_pricing(s0, k, t, sigma, r, cp, american=False, n = 100):

    #cijena call opcije u T CT = max(ST-K, 0)
    #cijena put opcije u T PT = max(K-ST, 0)
    
    #s0 - pocetna cijena
    #k - strajk cijena
    #t - datum dospjeca
    #v - volatility - promjenjivost -sigma
    #rf - risk-free rate
    #cp 1/-1 call/put
    #american True/False American/European
    #n - broj koraka binomnog stabla
    #b = B - money market account
    
    
    #jarrow-rudd algoritam za binomial tree 
    #ovi parametri se racunaju na razne nacine u ovisnosti od koristenja algoritma
    #(CRR, jarrow-rudd, Tian...)
    delta_t = t/n
    
    #p = 0.5
    u = math.exp((r-0.5*math.pow(sigma,2))*delta_t+sigma*math.sqrt(delta_t))
    d = math.exp((r-0.5*math.pow(sigma,2))*delta_t-sigma*math.sqrt(delta_t))
    
    b = math.exp(r*delta_t)
    q = (b - d)/(u-d) #q = p* - risk neutral measure
    
    st = np.zeros((n+1, n+1))
    option_value = np.zeros((n+1, n+1))
    st[0, 0] = s0
    am_price = []
    eu_price = []
    for i in range(1, n+1):
        st[i, 0] = st[i-1, 0]*u
        for j in range(1, i+1):
            st[i, j] = st[i-1, j-1]*d
            
         #rekurzija  
    for j in range(n+1):
        option_value[n, j] = max(0, cp*(st[n, j]-k)) #stavljanje maks. vrijednosti na kraj
    for i in range(n-1, -1, -1):
        for j in range(i+1): #European option
            option_value[i, j] = (q*option_value[i+1, j]+(1-q)*option_value[i+1, j+1])/b
            if american: #American option
                option_value[i, j] = max(option_value[i, j], cp*(st[i, j]-k))
                am_price.append(option_value[i, j]) #samo za potrebe plotanja
            else:
                eu_price.append(option_value[i, j]) #samo za potrebe plotanja
                
    #plotanje grafika 
    tam = np.linspace(0, 1, len(am_price))
    plt.plot(tam, am_price, 'bo')
    teu = np.linspace(0, 1, len(eu_price))
    plt.plot(teu, eu_price, 'ro')
    plt.show()
    
    return option_value[0,0]
    
    
V = option_pricing(100, 80, 1, 0.8, 0.01, -1, False, 10)
#V = option_pricing(100, 80, 1, 0.8, 0.01, -1, True, 100)
print(V)