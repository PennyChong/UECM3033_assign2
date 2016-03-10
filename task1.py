import numpy as np
import copy as cp

#Your optional code here
#You can import some modules or create additional functions

def optimalW(K): #determine the optimal value of omega, w in SOR method
    rad=max(np.abs(np.linalg.eigvals(K))) #compute the spectral radius of K
    w = 2*(1-np.sqrt(1-rad**2))/rad**2
    return w
    
    
def choice(A): #determine when to use LU factorization or SOR method
    temp=np.array(cp.copy(A),dtype=float)
    
    #check whether the SOR method is convergent
    #if convergent use SOR. Otherwise use LU factorization
    #SOR method converges for any x0 iff A is positive definite & symmetric
    
    for i in range(0,len(temp)):
        for j in range(i+1, len(temp)):
            if temp[i][j]!=temp[j][i]: #check symmetry property
                    return True #cannot use SOR if not symmetric, use LU
                    
        principal=np.array(cp.copy(temp[:i+1,: i+1])) #determine the principal submatrices
       
        if np.linalg.det(principal)<=0 : # check positive definite
            return True #cannot use SOR because not positive definite, use LU
                
    return False  # is positive definite and symmetric, hence use SOR         


def LUdecomp(A): #decompose A matrix into lower and triangular matrices
    n = len(A)
    for k in range(0, n-1):
        for i in range(k+1, n):
            if A[i,k] != 0.0:
                lam = A[i,k] / A[k,k]
                A[i, k+1:n] = A[i, k+1:n] - lam * A[k, k+1:n]
                A[i, k] = lam
    return A
    
    
def lu(A, b): # solve Ax=b with LU factorization
    sol = []
    # Edit here to implement your code
    b=np.array(cp.copy(b),dtype=float)
    A=np.array(cp.copy(A),dtype=float)
    A = LUdecomp(A)
    n = len(A)
    for k in range(1,n):
        b[k] = b[k] - np.dot(A[k,0:k], b[0:k])
    b[n-1]=b[n-1]/A[n-1, n-1]
    for k in range(n-2, -1, -1):
        b[k] = (b[k] - np.dot(A[k,k+1:n], b[k+1:n]))/A[k,k]
   
    sol=cp.copy(b)
    return list(sol)

def sor(A, b): # solve Ax=b with SOR method
    sol = []
    # Edit here to implement your code
    
    
    ITERATION_LIMIT=18  # number of iterations
    b=np.array(cp.copy(b),dtype=float)
    A=np.array(cp.copy(A),dtype=float)
    dgl= []
    
    for i in range(0,len(A)):
        dgl.append(A[i,i])
        
    D=np.array(np.diag(dgl))
    L_U=D-A  #A=D-L-U
    L=cp.copy(L_U)
    
    for i in range(0,len(L_U)):
        for j in range(i+1,len(L_U)):
            L[i][j]=0.0
            
     # calculate the optimal omega, w for higher convergence rate      
    w= optimalW((np.matrix(cp.copy(D),dtype=float).I)*np.matrix(cp.copy(L_U),dtype=float))
    msg='Optimal omega is %2.10f' %(w)  
    print(msg, end='\n')
    
    
    x=np.zeros_like(b)
    for itr in range(ITERATION_LIMIT): # perform sor method up to ITERATION LIMIT
        for i in range(len(b)):
            sums = np.dot( A[i,:], x )
            x[i] = x[i] + w*(b[i]-sums)/A[i,i]
        
    sol=cp.copy(x)
    
    return list(sol)

def solve(A, b):
    condition = choice(A)# State and implement your condition here
    if condition:
        print('Solve by lu(A,b)')
        return lu(A,b)
    else:
        print('Solve by sor(A,b)')
        return sor(A,b)

if __name__ == "__main__":
    ## import checker
    ## checker.test(lu, sor, solve)

    A = [[2,1,6], [8,3,2], [1,5,1]]
    b = [9, 13, 7]
    sol = solve(A,b)
    print(sol)
    
    A = [[6566, -5202, -4040, -5224, 1420, 6229],
         [4104, 7449, -2518, -4588,-8841, 4040],
         [5266,-4008,6803, -4702, 1240, 5060],
         [-9306, 7213,5723, 7961, -1981,-8834],
         [-3782, 3840, 2464, -8389, 9781,-3334],
         [-6903, 5610, 4306, 5548, -1380, 3539.]]
    b = [ 17603,  -63286,   56563,  -26523.5, 103396.5, -27906]
    sol = solve(A,b)
    print(sol)
    
 


  