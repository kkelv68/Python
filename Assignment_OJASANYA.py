#Name: Ojasanya Kehinde Ayomikun
#Date: 12/02/24
#Defining the nodal point
n = 4
#Defining the nodal spacing
h = 1 
#First order derivative
order = 1 
#Defining number of elements
e = n-1 
#Defining the boundary and input condition
v0 = 3

#Defining the nodal location
import pandas as pd
node = list(range(1, n+1))
location = [i * h for i in range(n)]
nodal_loc = pd.DataFrame({'node': node, 'location': location})
# print (nodal_loc)

#Defining element incidences
element = list(range(1, e+1))
node_1 = list(range(1, e+1))
node_2 = list(range(2, n+1))
element_ind = pd.DataFrame({'element': element, 'node_1': node_1, 'node_2': node_2})
print(element_ind)

#Defining the element matrices
import numpy as np
#using zeros to create the 4x4 matrix that will be used for the iterative results from the element matrices
global_mat = np.zeros((4, 4))
#there are 3 elements and a discharge value Q of 1 is applied to each end node of the element
Q = 1 
Q_mat = np.full((3, 1), Q)

#Iterate over each element
for i in range(e):
    #retrieve the position of the initial node to position the element matrix within the global matrix.
    initial_node = element_ind['node_1'][i]
    #retrieve the position of the final node to position the element matrix within the global matrix.
    final_node = element_ind['node_2'][i]
    #calculate the length of each element using the location matrix (h will still work due to equal length)
    #the value of "i+1" indicates the position of the final node of the element, 
    #while "i" denotes the location of the initial node
    len_ele = nodal_loc['location'][i+1] - nodal_loc['location'][i]
    #Create the element matrix
    element_mat = np.array([[-1/len_ele, 0], [1/len_ele, 0]])

    #The global matrix using values from the element matrix was updated
    #Initially identified the specific location within the matrix where the element matrix is to be inserted
    global_mat[initial_node-1:final_node-1, initial_node-1:final_node-1] + element_mat

#The global matrix is updated for each element iteration
print(global_mat)


#Obtaining the first column of the global matrix, excluding the last row
matrix_reduction = global_mat[0:n-1, 0]
#Converting to a matrix
matrix_reduction = np.array(matrix_reduction)
#Using the boundary condition (v0)
matrix_reduction *= v0
#Modifying the Q matrix
Q_mat -= matrix_reduction
#Global matrix reduction
global_mat = global_mat[0:n-1, 1:n]
#0:n-1 represents rows from row 0 to n-2 (excluding last row),
#1:n represents columns from column 1 to n (excluding first column)


#Calculate velocity result using matrix inversion
velocity_result = np.linalg.solve(global_mat, Q_mat)

#The numpy function np.linalg.solve() performs the equivalent of solving Ax = b, where A is the global matrix,
#x is the velocity_result, and b is the Q_mat.

