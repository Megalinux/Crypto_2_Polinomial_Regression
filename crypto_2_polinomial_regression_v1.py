import numpy as np      
import pandas as pd
from pylab import plt,mpl
import ccxt
import calendar
from datetime import datetime
from sympy import Symbol,expand
import tools as tl

#Set parameters of Matplotlib
np.random.seed(100)
plt.style.use('seaborn')
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'

#Uses the binance method of the ccxt library to download the data
binance = ccxt.binance()
now = datetime.utcnow()

unixtime = calendar.timegm(now.utctimetuple())
da = (unixtime - 300*300) * 1000 

ohlcv = binance.fetch_ohlcv(symbol='ETH/BTC', timeframe='5m',since=da)
df1 = pd.DataFrame(ohlcv, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
df1['Time'] = [datetime.fromtimestamp(float(time)/1000) for time in df1['Time']]
df1.set_index('Time')

#Set the resample interval of 15 minute
df1_risultato = df1.resample('15T', on = 'Time').mean()

#View the 'Close' price chart of the ETH / BTC pair of the Binance exchange
df1_risultato.plot(y='Close',figsize=(10,6), title="ETH/BTC Close Price")
plt.show()

#Perform standardization
l = df1_risultato['Close'].values
l = (l-l.mean()) / np.std(l)
f = np.linspace(-2,2, len(l))

#Displays the standardized values ​​of the ETH / BTC cryptocurrency pair
plt.figure(figsize=(10,6))
plt.plot(f,l,'ro')
plt.title('Standardized values of ETH/BTC Close Price')
plt.xlabel('Time')
plt.ylabel('Labels: Price')
plt.show()

#Calculate the fifth degree equation with the estimated coefficients
reg = np.polyfit(f,l,deg=5)
equazione = np.poly1d(reg)
x=Symbol('x')
print(expand(equazione(x)))

#Calculate the approximate functions of the third, fifth and seventh degree
p = np.polyval(reg,f) 
reg1 = np.polyfit(f,l,deg=3) 
reg2 = np.polyfit(f,l,deg=7) 
p1 = np.polyval(reg1,f) 
p2 = np.polyval(reg2,f) 

#Print MSE values
tl1 = tl.Tools()
print('%.12f' % tl1.MSE(l,p)) 
print('%.12f' % tl1.MSE(l,p1)) 
print('%.12f' % tl1.MSE(l,p2)) 

#Displays the approximation functions
plt.figure(figsize=(10,6))
plt.plot(f,l,'ro',label='real values')
plt.plot(f,p1,'--', label = 'regression 3 degree')
plt.plot(f,p, '--', label = 'regression 5 degree') 
plt.plot(f,p2,'--', label = 'regression 7 degree')
plt.legend()


#Set the labels in the fifth degree function
"""for a,b in zip(f, p2): 
    plt.text(a, b, "{:.12f}".format(b))"""
plt.show()

#Calculate the step of 15 minute for the future value
c = 2 / f.size
d = 2+c

#Calcolate the future value (in this case 15 minute) of the seventh degree function.
predetto7grado = np.polyval(reg2,d)
print('Future 15 minute value of price ETH/BTC: ')
print('%.12f' % predetto7grado) 


