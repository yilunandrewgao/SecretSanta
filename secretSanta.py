import numpy as np
import pygraphviz as pgv
import tarjan

LARGE_NUM = 10

def get_input():
	
	numV = int(input().strip())
	graphMatrix = np.zeros((5,5))
	# get matrix representation of graph:
	for i in range(numV):
		graphMatrix[i] = list(map(int, input().split()))
	return (numV, graphMatrix)

# make nice lettering for nodes
def make_num_to_letter_dict(numV):

	Dict = {}
	Dict[0] = "source"
	Dict[2*numV+1] = "sink"
	for i in range(1,2*numV+1):
		if (i-1)//numV > 0:
			Dict[i] = chr(i-numV+96) + " prime"
		else:
			Dict[i] = chr(i+96)
	return Dict


# uses pygrahpviz to visualize graph
def draw_graph(numV, matrix, filename):
	A=pgv.AGraph(directed = True)

	length = len(matrix)
	Dict = make_num_to_letter_dict(numV)

	for i in range(length):
		for j in range(length):
			if matrix[i][j]:
				A.add_edge(Dict[i], Dict[j], label = str(matrix[i][j]), weight = matrix[i][j])

	A.layout(prog='dot')
	A.draw(filename)

#create a flow network with 2 layers of everyone
def create_flow_network(matrix):

	numV = len(matrix)

	flow_matrix = np.zeros((2*numV+2, 2*numV+2))
	for i in range(1):
		for j in range(1, numV+1):
			flow_matrix[i][j] = 1

	for i in range(1, numV+1):
		for j in range(numV+1, 2*numV+1):
			flow_matrix[i][j] = matrix[i-1][j-numV-1] * LARGE_NUM
	
	for i in range(numV+1, 2*numV+1):
		for j in [2*numV+1]:
			flow_matrix[i][j] = 1

	return flow_matrix






def main():

	numV, graph = get_input()

	print (graph)

	flow_matrix = create_flow_network(graph)
	draw_graph(numV, flow_matrix, "original_flow.png")

	flow_graph, flow = tarjan.getFlow(2*numV+2, 0, 2*numV+1, flow_matrix)
	print (flow)

	draw_graph(numV, flow_graph, "found_flow.png")


if __name__ == "__main__":
	main()