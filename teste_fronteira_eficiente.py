import yfinance
import pandas as pd
import numpy as np
import datetime as dt
import quandl
from matplotlib import pyplot as plt
import scipy.optimize as solver
ativos = ['ETH-USD','WEGE3.SA','SLCE3.SA','ELP','BBAS3.SA','SID']
df = yfinance.download(ativos, start='2017-01-01', end=dt.datetime.now())['Adj Close']
df = df.dropna()
print(df)

weight = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]

retornos = df.pct_change().dropna()
retorno_carteira = pd.Series((retornos*weight).sum(axis=1), name='portfolio')
print(retorno_carteira)
plt.plot(retorno_carteira)
plt.show()
plt.clf()

retorno_acumulado = (1+retornos).cumprod()
retorno_acumulado = (retorno_acumulado*weight).sum(axis=1)
plt.plot(retorno_acumulado)
plt.show()
plt.clf()

#numero de ativos
j = len(df.columns)
list = df.columns

df = df.pct_change()

mi = df.mean()*252
sigma = df.cov()*252

vet_ret = []
vet_vol = []
vet_pesos = []
for i in range(2000):
    w = np.random.random(j)
    w = w/np.sum(w)
    retorno = np.sum(w * mi)
    risco = np.sqrt(np.dot(w.T, np.dot(sigma, w)))
    vet_pesos.append(w)
    vet_ret.append(retorno)
    vet_vol.append(risco)

vet_pesos = pd.array(vet_pesos)
vet_vol = pd.array(vet_vol)
vet_ret = pd.array(vet_ret)
data = {'pesos': vet_pesos, 'retorno': vet_ret, 'volatilidade': vet_vol}

df_vet = pd.DataFrame(data)

print(df_vet)

#Fronnteira Eficiente Grafico

def f_obj(peso):
    return np.sqrt(np.dot(peso.T,np.dot(sigma,peso)))

x0 = np.array([1.0 / (len(list)) for x in range(len(list))])

bounds = tuple((0,1) for x in range(len(list)))

faixa_ret = np.arange(0.26, 0.64, .01)

risk = []

for i in faixa_ret:
    constraints = [{'type': 'eq', 'fun' : lambda x: np.sum(x) - 1},
                   {'type': 'eq', 'fun' : lambda x: np.sum(x*mi) - i}]
    outcome = solver.minimize(f_obj, x0, constraints=constraints, bounds=bounds, method='SLSQP')
    risk.append(outcome.fun)

print('')
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('pesos otimos (w) =', outcome['x'].round(3))
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('')
print(outcome)
w = outcome['x'].round(3)
retorno = np.sum(w * mi)
risco = np.sqrt(np.dot(w.T, np.dot(sigma, w)))

plt.plot(risk, faixa_ret, 'r--x', linewidth=5)
plt.xlabel("Risco", fontsize = 14)
plt.ylabel("Retorno", fontsize = 14)
plt.show()
plt.clf()

print('')
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('pesos otimos (w) =', outcome['x'].round(3))
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('')

#Ponto òtimo - Minima Volatilidade

def estatistica_port(peso):
    peso = np.array(peso)
    ret_ot = np.sum(peso*mi)
    risco_ot = np.sqrt(np.dot(peso.T,np.dot(sigma, peso)))
    return np.array([ret_ot,risco_ot])

for i in faixa_ret:
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
                   #{'type': 'eq', 'fun': lambda x: np.sum(x * mi) - i}]
    outcome = solver.minimize(f_obj, x0, constraints=constraints, bounds=bounds, method='SLSQP')
    risk.append(outcome.fun)

ret_ot, risco_ot = estatistica_port(outcome['x'])
print('Retorno otimo esperado = ', str((ret_ot*100).round(3)) + '%')
print('volatilidade otima esperada  = ', str((risco_ot*100).round(3)) + '%')
print('Sharp ratio otimizado = ', str(((ret_ot/risco_ot)*100).round(3)) + '%')


