/*
	Name: Michael Welford
	File Name: funcwithpointers.c
*/
#include <stdio.h>

// Declare functions that use and return pointers.
int add_up (int *ar, int num_elements);
int *add_one(int *ar, int num_elements);

// A program to practice working with functions that use pointers.
int main()
{
	// Declare and initialize an array a.
	int a[3] = {1,2,3};
	
	Print the total of the values in a.
	printf("%d\n", add_up(a,3));
	
	// Get a pointer to an integer.
	int *b = add_one(a,3);
	
	// Print the corresponding values in a and b.
	for (int i = 0; i < 3; i++)
		printf("%d  %d\n",a[i],b[i]);
	
	
	return 0;
}

/***
 A function that takes a pointer to an int and the number of elements
 and adds up the values.
 
 Parameters: ar - a pointer to an int
             num_elements - the integer number of elements to sum.
			 
 Returns: total - the integer total of the numbers.
***/
int add_up (int *ar, int num_elements)
{
	// Initiatlize the total and index used.
	int total = 0;
	int k;
	
	// Sum the elements. The points starts at index 0 with an array is passed.
	for (k = 0; k < num_elements; k++)
	{
		total += ar[k];
	}
	
	// Return the total.
	return total;
}

/***
 A function that fills an array of ints and returns a pointer to the first value
 in the array.
 
 Parameters: ar - a pointer to an integer
             num_elements - the number of elements to iterate over
 Returns:    b - the pointer to the first element of array b.
***/
int *add_one(int *ar, int num_elements)
{
	static int b[3];
	
	for (int i = 0; i < num_elements; i++)
	{
		b[i] = ar[i] + 1;
	}
	
	return (b);
}