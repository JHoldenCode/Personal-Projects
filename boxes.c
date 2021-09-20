#include <stdio.h>
#include <stdlib.h>

enum bool{ FALSE, TRUE };
typedef enum bool Boolean;

Boolean doesFit(int small, int large, int dims);
void sort(int* arr, int dims);
Boolean compare(int* smallArr, int* largeArr, int dims);
void longestPath(FILE * pData, int boxes, int dims);
void topSort(int exploringNode, int* nodesLeftArr, int* numNodesLeft, int* sortedArr, int* numInSortedArr, int dims, int boxes);
void removeAndShift(int* nodesLeftArr, int* numNodesLeft, int shiftTo);
int findPath(int* treeArr, int totalTrees, int* treePath, int treesInPath, int index, int dims, int * maxPath, int * currentLongestPath);

int main(int argc, char* argv[])
{
	FILE* pData;
	int noc, numBoxes, dimensions;

	//open file
	pData = fopen("boxData.txt", "r");
	if (pData == NULL)
	{
		printf("Error: did not open file");
		exit(1);
	}

	//check if there is another sequence
	noc = fscanf(pData, "%d", &numBoxes);
	while (noc == 1)
	{
		//retrieve sequence parameters
		fscanf(pData, "%d", &dimensions);
		//find the longest path
		longestPath(pData, numBoxes, dimensions);
		//check case
		noc = fscanf(pData, "%d", &numBoxes);
	}

	//close file
	fclose(pData);

	return 0;
}

void longestPath(FILE* pData, int boxes, int dims)
{
	int path;
	int currentLongestPath = 0;
	int maxPath[30];
	int pathArr[30];
	FILE* pThisSeq;
	int i, num;
	int numNodesLeft = boxes;
	int nodesLeftArr[30];
	int sortedArr[30];
	int numInSortedArr = 0;
	//write box data to other file
	pThisSeq = fopen("thisSequence.txt", "w");
	for (i = 0; i < boxes * dims; i++)
	{
		fscanf(pData, "%d", &num);
		fprintf(pThisSeq, "%d ", num);
	}
	fclose(pThisSeq);
	//make nodesLeftArr
	for (i = 1; i <= boxes; i++)
	{
		nodesLeftArr[i - 1] = i;
	}
	//topologically sort
	while (numNodesLeft > 0)
	{
		topSort(-1, nodesLeftArr, &numNodesLeft, sortedArr, &numInSortedArr, dims, boxes);
	}
	//recursively find max path
	path = findPath(sortedArr, boxes, pathArr, 0, 0, dims, maxPath, &currentLongestPath);
	//print results
	printf("%d\n", path);
	for (i = 0; i < path; i++)
	{
		printf("%d ", maxPath[i]);
	}
	printf("\n");
}

void topSort(int exploringNode, int* nodesLeftArr, int* numNodesLeft, int * sortedArr, int* numInSortedArr, int dims, int boxes)
{
	int i = 0;
	int currentNode;
	if (exploringNode > 0)
	{
		currentNode = exploringNode;
	}
	else
	{
		currentNode = nodesLeftArr[0];
		//gets rid of current node in available nodes list
		removeAndShift(nodesLeftArr, numNodesLeft, 0);
	}
	//cycle through all possible nodes
	while (i < *numNodesLeft)
	{
		if (!doesFit(currentNode - 1, nodesLeftArr[i] - 1, dims))
		{
			i++;
		}
		else
		{
			int nextNode = nodesLeftArr[i];
			//printf("%d ", nextNode);
			removeAndShift(nodesLeftArr, numNodesLeft, i);
			topSort(nextNode, nodesLeftArr, numNodesLeft, sortedArr, numInSortedArr, dims, boxes);
		}
	}
	//add node once all paths exhausted
	sortedArr[boxes - *numInSortedArr - 1] = currentNode;
	*numInSortedArr = *numInSortedArr + 1;
}

void removeAndShift(int* nodesLeftArr, int* numNodesLeft, int shiftTo)
{
	int i;
	for (i = shiftTo + 1; i < *numNodesLeft; i++)
	{
		nodesLeftArr[i - 1] = nodesLeftArr[i];
	}
	*numNodesLeft = *numNodesLeft - 1;
}

int findPath(int* treeArr, int totalTrees, int* treePath, int treesInPath, int index, int dims, int * maxPath, int * currentLongestPath)
{
	int newPathArr[30];
	int leftMax, rightMax, i;
	if (treesInPath > *currentLongestPath)
	{
		*currentLongestPath = treesInPath;
		for (i = 0; i < treesInPath; i++)
		{
			maxPath[i] = treePath[i];
		}
	}
	//base cases
	if (index >= totalTrees)
	{
		return treesInPath;
	}
	//make arr
	for (i = 0; i < treesInPath; i++)
	{
		newPathArr[i] = treePath[i];
	}
	//call left and right again
	rightMax = findPath(treeArr, totalTrees, newPathArr, treesInPath, index + 1, dims, maxPath, currentLongestPath);
	if (treesInPath == 0)
	{
		newPathArr[0] = treeArr[index];
		leftMax = findPath(treeArr, totalTrees, newPathArr, treesInPath + 1, index + 1, dims, maxPath, currentLongestPath);
	}
	else if (!doesFit(newPathArr[treesInPath - 1] - 1, treeArr[index] - 1, dims))
	{
		return rightMax;
	}
	else
	{
		newPathArr[treesInPath] = treeArr[index];
		leftMax = findPath(treeArr, totalTrees, newPathArr, treesInPath + 1, index + 1, dims, maxPath, currentLongestPath);
	}
	//return longer path
	if (leftMax > rightMax)
	{
		return leftMax;
	}
	else
	{
		return rightMax;
	}
}





Boolean doesFit(int small, int large, int dims)
{
	//open file
	FILE* pThisSeq;
	int smallArr[30];
	int largeArr[30];
	int i, val;

	//create small list
	pThisSeq = fopen("thisSequence.txt", "r");
	if (pThisSeq == NULL)
	{
		printf("Error: file did not open");
		exit(1);
	}
	for (i = 0; i < dims * small; i++)
	{
		fscanf(pThisSeq, "%d", &val);
	}
	for (i = 0; i < dims; i++)
	{
		fscanf(pThisSeq, "%d", &val);
		smallArr[i] = val;
	}
	fclose(pThisSeq);

	//create large list
	pThisSeq = fopen("thisSequence.txt", "r");
	if (pThisSeq == NULL)
	{
		printf("Error: file did not open");
		exit(1);
	}
	for (i = 0; i < dims * large; i++)
	{
		fscanf(pThisSeq, "%d", &val);
	}
	for (i = 0; i < dims; i++)
	{
		fscanf(pThisSeq, "%d", &val);
		largeArr[i] = val;
	}
	fclose(pThisSeq);

	//sort both lists
	sort(smallArr, dims);
	sort(largeArr, dims);

	//compare lists
	return compare(smallArr, largeArr, dims);
}

void sort(int * arr, int dims)
{
	int high, highInd, i, temp;
	high = -1;
	while (dims > 1)
	{
		//find highest value
		for (i = 0; i < dims; i++)
		{
			if (arr[i] > high)
			{
				high = arr[i];
				highInd = i;
			}
		}

		//switch to last place
		if (highInd != dims - 1)
		{
			temp = arr[dims - 1];
			arr[dims - 1] = high;
			arr[highInd] = temp;
		}
		high = -1;
		dims--;
	}
}

Boolean compare(int * smallArr, int * largeArr, int dims)
{
	int i;
	for (i = 0; i < dims; i++)
	{
		if (smallArr[i] >= largeArr[i])
		{
			return FALSE;
		}
	}
	return TRUE;
}