# coding=utf-8
import math
from random import randrange

#Eduardo Rubio Lezama
#Luis Enrique Cortez Flores

#Algoritmo RSA para cifrar, el metodo generaPrimo(n) se encarga de generar primos de n digitos,
# donde para verificar si n es primo ocupamos SolovayStrassen 
# 
# El programa se ejecuta con main(nDigitos, texto) donde nDigitos es el numero de digitos que 
#queremos que tengan tanto p como q y texto, el texto a cifrar
#
# Ejecutar en consola con python RSA.py

##Atributos del algoritmo RSA
p_RSA = 0
q_RSA = 0
n_RSA = 0
e_RSA = 0
d_RSA = 0
phiN_RSA = 0
alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']



def main(nDigitos, texto):
	global p_RSA
	global q_RSA
	global n_RSA
	global phiN_RSA	
	global alfabeto
	while True:
		
		p_RSA = generaPrimo(nDigitos)
		q_RSA = generaPrimo(nDigitos)
		if p_RSA != q_RSA:
			break

	n_RSA = p_RSA*q_RSA
	phiN_RSA = (p_RSA-1)*(q_RSA-1)

	escoge_e()
	escoge_d()
	
	print ("Paramatros generados por RSA:")
	print ("p:" + str(p_RSA) + "; q:" + str(q_RSA) + "; n:" + str(n_RSA) + "; e:" + str(e_RSA) + "; d:" + str(d_RSA))

	print ("\n")
	print ("Texto cifrado: ")
	cifrado=[]
	for i in range(len(texto)):
		cifrado.append(cifraRSA(encuentraIndice(texto[i])))
	print(cifrado)


	print ("\n")
	print ("Texto descifrado: ")
	descifrado=[]
	alfabetoD=[]
	for i in range(len(cifrado)):
		descifrado.append(descifraRSA(cifrado[i]))

	for j in range(len(descifrado)):
		alfabetoD.append(alfabeto[descifrado[j]])
	print(alfabetoD)

# Funcion que calcula el AEE extendido de Euclides para dos numeros, regresa una tripleta (d,x,y)
# donde: d= ax + by , d = mcd(a,b) 
def AEE(a, b):
	
	d = 0
	x = 0 
	y = 0
	if (b == 0): 
		
		d = a
		x = 1
		y = 0
		return [d,x,y]
		
		

	x1 = 0 
	y1 = 1 
	x2 = 1 
	y2 = 0

	while (b > 0): 
		
		q = int(a / b)
		r = a - (q*b)
		x = x2 - (q*x1)
		y = int(y2 - (q*y1))
		a = b
		b = r
		x2 = x1
		x1 = x
		y2 = y1
		y1 = y
		

	d = a
	x = x2
	y = y2
		
	tripleta = [d,x,(y+phiN_RSA) % phiN_RSA]
	#print (tripleta)

	return tripleta
			

#implementacion de Solovay	
def Solovay(n):
	bandera = False
	for i in range(5):
		
		a = randrange(2,n-2)
		
		u = pow(a,int((n-1)/2)) % n
		if u == n-1:
			u = -1
		v = Jacobi(a,n)
		
			
		if u != v:
			break
		bandera = True	
	return bandera	

## Funcion encargada de generar el valor "e" del algoritmo RSA	
def escoge_e():
	global e_RSA
	global phiN_RSA
	while True: 
		e_RSA = randrange(1,phiN_RSA - 1)
		if AEE(phiN_RSA , e_RSA)[0] == 1:
	 		break

	#print (e_RSA)		


#Funcion que genera el valor de "d" del algoritmo RSA
def escoge_d():
	#print ("phideN: "+str(phiN_RSA) + "e: " + str(e_RSA))
	global d_RSA
	d_RSA = AEE(phiN_RSA,e_RSA)[2]
	#print (AEE(phiN_RSA,e_RSA))
	#print (d_RSA)
	

#Funcion encargada de la generacion de numeros de n digitos
def generaNumero(nDigitos):
	
	n = randrange((pow(10,(nDigitos-1))/2)+4, pow(10,nDigitos)/2)
	n = (2*n) + 1
	if (n%5) == 0:
		n += 2

	return n

#MEtodo que te genera un posible numero primo, el posible es cuando el numero es muy grande
def generaPrimo(nDigitos):

	es_primo = False	
	n = 0
	while True:
	
		n = generaNumero(nDigitos)
					
		es_primo = Solovay(n)
				
		if es_primo:
			break
				
	return n			
	

#Metodo para calcular la factorizacion de un numero
def calculaFactores(n):
		
	n1 = n
	exponente = 0
	raiz = int(math.sqrt(n))
	#arreglo que guarda los factores de n
	exponentes = []
	i = 2
	si = i
	if n==2 or n == 3:
		return [[n,1]]

	while(True):
		pi = 0
		while (n%si == 0):
			pi += 1
			if pi== 1:
				
				exponentes.append([si,pi])
			else:
				exponentes[len(exponentes)-1] = [si,pi] 	
			
			n = int(n/si)
		
		if (si == raiz):
			exponentes.append([n,1])
			break
		
		i +=1
		si = i

	return exponentes	



#Funcion que calcula el simbolo de Legendre de un primo
def LegendreP(p,m):
	if (pow(p,(m-1)/2) % m) > 1:
		return -1
	return pow(p,(m-1)/2) % m

#funcion que calcula el simbolo de Jacobi, primero factorizamos n y aplicamos simobolo de Legendre a cada factor de a
def Jacobi(a,m):
	factores = calculaFactores(a)
	
	jacobi = 1
	for i in range(len(factores)):
		jacobi *=  pow (LegendreP(factores[i][0],m),factores[i][1]) 
	return jacobi		

#Dado una letra, te dice que numero le corresponde
def encuentraIndice(letra):
	global alfabeto
	for i  in range (len(alfabeto)):
		if(alfabeto[i]==letra):
			return i


# Funcion para cifrar RSA
def cifraRSA(m):
	c = pow(m,e_RSA) % n_RSA
	return c		



#Funcion para descifrar RSA
def descifraRSA(c):
	m = pow(c,d_RSA) % n_RSA
	return m

			
if __name__ == '__main__':
	
	main(2,"holaestoesrsa")
	


	