import codecs

'''
INPUT: Dateiname der Datei mit den Matrix-Daten. 
		Form: 	x1;x2;x3
				y1;y2;y3
				...
OUTPU: MATRIX[][]
'''
def readMatrix(filename):
	matrix = []
	inputFile = codecs.open(filename, 'r')
	string = inputFile.read()
	rows = string.split("\n")
	
	for row in rows:
		elements = row.split(";")
		newRow = []
		try:
			for element in elements:
				newRow.append(int(element))
			matrix.append(elements)
		except: 
			continue
	
	matrix = [[int(e) for e in row] for row in matrix]
	
	return matrix

def printMatrix(matrix):
	for row in matrix:
		print row
