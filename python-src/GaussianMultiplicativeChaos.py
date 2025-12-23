import numpy as np
import matplotlib.pyplot as plt

def gaussian_multiplicative_chaos(N=3000,gamma=0.9,L=1.0):
	x=np.linspace(0,L,N)
	k=np.fft.fftfreq(N,d=L/N)
	k[0] = 1.0
	#Log-correlated Gaussian field
	randomphase=np.random.normal(size=N) + 1j*np.random.normal(size=N)
	X_hat = randomphase/np.sqrt(np.abs(k))
	X = np.real(np.fft.ifft(X_hat))
	var_X = np.var(X)
	gmc = X*np.exp(gamma*X - 0.5*gamma**2*var_X)
	gmc = gmc/np.sum(gmc)
	return (x,gmc)

if __name__=="__main__":
	x,gmc=gaussian_multiplicative_chaos()
	plt.plot(x,gmc)
	plt.xlabel("x")
	plt.ylabel("GMC")
	plt.show()



