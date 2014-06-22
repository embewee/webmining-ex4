import readmatrix

def rowSum(matrix, row):
	rowSum = 0
	for i in range(0, len(matrix[row])):
		rowSum += matrix[row][i]
	return rowSum
		
def colSum(matrix, col):
	colSum = 0
	for i in range(0, len(matrix)):
		colSum += matrix[i][col]
	return colSum

def diagSum(matrix):
	diagSum = 0
	for i in range(0, len(matrix)):
		diagSum += matrix[i][i]
	return diagSum

def quality(matrix):
	nrOfCols = len(matrix)
	matrixSum = 0;
	for i in range(0, nrOfCols):
		matrixSum += rowSum(matrix, i)

	print "matrix sum=" + str(matrixSum)

	#[TP][FP]
	#[FN][TN]
	sumTP = 0;
	sumFP = 0;
	sumFN = 0;
	sumTN = 0;

	for i in range(0, nrOfCols):
		#print "Class " + str(i)
		TP = matrix[i][i]
		FP = rowSum(matrix, i) - matrix[i][i]
		FN = colSum(matrix, i) - matrix[i][i]
		TN = matrixSum - TP - FP - FN
		#print "TP=" + str(TP) + ", FP=" + str(FP) + ", FN=" + str(FN) + ", TN=" + str(TN)
		sumTP += TP
		sumFP += FP
		sumFN += FN
		sumTN += TN

	print "avg TP=" + str(sumTP)
	print "avg FP=" + str(sumFP)
	print "avg FN=" + str(sumFN)
	print "avg TN=" + str(sumTN)

	print "diagSum=" + str(diagSum(matrix))

	accuracy = float(diagSum(matrix)) / float(matrixSum)
	microAvgPrecision = float(sumTP) / float(float(sumTP) + float(sumFP))
	microAvgRecall = float(sumTP) / float(float(sumTP) + float(sumFN))
	microAvgF1 = float(2 * microAvgRecall * microAvgPrecision) / float(microAvgRecall + microAvgPrecision)

	print "accuracy=" + str(accuracy)
	print "microAvgPrecision=" + str(microAvgPrecision)
	print "microAvgRecall=" + str(microAvgRecall)
	print "microAvgF1=" + str(microAvgF1)

############################
# SKRIPT ###################
############################
matrix = readmatrix.readMatrix("KONFUSIONSMATRIX-knn15.DATA")
quality(matrix)

print "##############################################"

matrix = readmatrix.readMatrix("KONFUSIONSMATRIX-knn10.DATA")
quality(matrix)

print "##############################################"

matrix = readmatrix.readMatrix("KONFUSIONSMATRIX-knn5.DATA")
quality(matrix)
