import readmatrix

def rowSum(matrix, row):
	rowSum = 0;
	for i in range(0, len(matrix[row])):
		rowSum += matrix[row][i]
	return rowSum
		
def colSum(matrix, col):
	colSum = 0;
	for i in range(0, len(matrix)):
		colSum += matrix[i][col]
	return colSum

matrix = readmatrix.readMatrix("KONFUSIONSMATRIX.DATA")
nrOfCols = len(matrix)
matrixSum = 0;
for i in range(0, nrOfCols):
	matrixSum += rowSum(matrix, i)

print "matrix sum=" + str(matrixSum)

#[TP][FP]
#[FN][TN]
TP = 0;
FP = 0;
FN = 0;
TN = 0;

for i in range(0, nrOfCols):
	TP =+ matrix[i][i]
	FP =+ rowSum(matrix, i) - matrix[i][i]
	FN =+ colSum(matrix, i) - matrix[i][i]
	TN =+ matrixSum - TP - FP - FN

print "TP=" + str(TP)
print "FP=" + str(FP)
print "FN=" + str(FN)
print "TN=" + str(TN)


