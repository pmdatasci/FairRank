import numpy as np
from numpy.lib import nanpercentile


def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    '''
    R: rating matrix
    P: |U| * K (User features matrix)
    Q: |D| * K (Item features matrix)
    K: latent features
    steps: iterations
    alpha: learning rate
    beta: regularization parameter'''
    
    Q = Q.T


    # PMC - count iterations
    x = 0
    # PMC - set break condition
    break_val = 1

    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    # calculate error
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])

                    for k in range(K):
                        # calculate gradient with a and beta parameter
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        eR = np.dot(P,Q)

        e = 0


        for i in range(len(R)):

            for j in range(len(R[i])):

                if R[i][j] > 0:

                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)

                    for k in range(K):

                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
                        x= x+1
        # 0.001: local minimum


        if e < break_val:
            print('breaking')

            break

    print(f'Iterations to minimise: {x}')    

    return P, Q.T


def main():

        R = [   [5,3,0,1],
                [4,0,0,1],
                [1,1,0,5],
                [1,0,0,4],
                [0,1,5,4],
                [2,1,3,0],    ]

        R = np.array(R)
        # N: num of User
        N = len(R)
        # M: num of Movie
        M = len(R[0])
        # Num of Features
        K = 3

 
        P = np.random.rand(N,K)
        Q = np.random.rand(M,K)

 

        nP, nQ = matrix_factorization(R, P, Q, K)

        nR = np.dot(nP, nQ.T)

        print(nR)

        return

if __name__ == "__main__":
    main()
