/*
	Name: Michael Welford
	File Name: arrays.c
*/
#include <stdio.h>

// A program to demonstrate arrays in c.
int main()
{
	// An array of integers of size 10.
	int ar_One[10];
	
	// An array of floats of size 5.
	float ar_Two[5] = {1.2,1.4,1.6,1.8,2.0};
	
	// Declaration of a 3x2 multidimensional array of floats.
	float ar_Three[3][2];
	
	// Printing the value at index 1 to 1 digit.
	printf("%3.1f\n",ar_Two[1]);
	
	// Loop over the first array.
	for (int i = 0; i< 10; i++)
	{
		// Increment each value in the array.
		ar_One[i] = i+1;
		
		// Print the value.
		printf("%d\n", ar_One[i]);
	}
	
	// Initialize index j to 0.
	int j = 0;
	
	// For index i = 0  while i < 5, increment by 2.
	for (int i = 0; i < 5; i+=2)
	{
		// If i equals 4:
		if (i == 4)
			
			// Set the value in ar_Three[j][0] to the value in ar_Two[i]
			ar_Three[j][0] = ar_Two[i];
			
		// Otherwise:
		else
		{
			// Set the value in ar_Three[j][0] to the value in ar_Two[i]
			// and set the value in ar_Three[j][1] to ar_Two[i+1]
			ar_Three[j][0] = ar_Two[i];
			ar_Three[j][1] = ar_Two[i+1];
		}
		
		// Increment j by 1.
		j++;
	}
	
	// Another example of assigning in a two-dimensional array.
	ar_Three[2][1] = 2.2;
	
	// Print all the values in ar_Three.
	for (int i = 0; i<3; i++)
		for(int j = 0; j<2; j++)
		{
			printf("%3.1f\n",ar_Three[i][j]);
		}
	End the program.	
	return 0;
}