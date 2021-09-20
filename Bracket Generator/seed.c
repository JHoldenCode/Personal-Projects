#include <stdio.h>
#include <math.h>

int enterNum();
void make(int* bracket, int seeds, int currentRound);
void print(int *bracket);

int main(int argc, char* argv[])
{
	int i;
	int bracket[1000];
	int seeds;
	seeds = enterNum();
	make(bracket, seeds, 1);
	printf("\n");
	print(bracket);
}

int enterNum()
{
	int x;
	printf("Enter number of seeds: ");
	scanf("%d", &x);
	return x;
}

void make(int* bracket, int seeds, int currentRound)
{
	int a[1000];
	int b[1000];
	int i;
	for (i = 0; i < 1000; i++)
	{
		if (i == 0 || i == 1)
			a[i] = i + 1;
		else
			a[i] = -1;
	}
	for (i = 0; i < 1000; i++)
	{
		if (i == 0 || i == 1)
			b[i] = i + 1;
		else
			b[i] = -1;
	}
	while (seeds > pow(2, currentRound))
	{
		int indexLast = 0;
		int indexCurrent = 0;
		if (currentRound % 2 == 0)
		{
			while (b[indexLast] > 0)
			{
				a[indexCurrent] = b[indexLast];
				a[indexCurrent + 1] = pow(2, currentRound + 1) + 1 - a[indexCurrent];
				indexCurrent += 2;
				indexLast++;
			}
		}
		else
		{
			while (a[indexLast] > 0)
			{
				b[indexCurrent] = a[indexLast];
				b[indexCurrent + 1] = pow(2, currentRound + 1) + 1 - b[indexCurrent];
				indexCurrent += 2;
				indexLast++;
			}
		}
		currentRound++;
	}
	for (i = 0; i < 1000; i++)
	{
		if (currentRound % 2 == 0)
			if (b[i] <= seeds)
				bracket[i] = b[i];
			else
				bracket[i] = 0;
		else
			if (a[i] <= seeds)
				bracket[i] = a[i];
			else
				bracket[i] = 0;
	}
	
}

void print(int *bracket)
{
	int matchup = 0;
	int i = 0;
	while (bracket[i] >= 0)
	{
		if (bracket[i + 1] == 0)
			printf("%d\n", bracket[i]);
		else
			printf("%d\n%d\n", bracket[i], bracket[i + 1]);
		i += 2;
		printf("------\n");
	}
}
