/*
	Name: Michael Welford
	File Name: recursion.c
*/
#include <stdio.h>

// Declare functions.
int factorial(int);

// A function to practice recursion.
int main()
{
	//Declare an integer a.
	int a;
	
	// Get a value from stdin for a.
	printf("Input an integer: ");
	scanf("%d", &a);
	
	// Print a!.
	printf("The value of %d! is %d.", a, factorial(a));
	return 0;
}

/***
 A recursive function to calculate a factorial.
 
 Parameters: num - the integer we want to find the factorial of.
 
 Returns: the factorial of num as an integer
***/
int factorial(int num)
{
	// If num equals 1, return 1.
	if (num == 1)
		return 1;
	
	// Otherwise, get the factorial.
	// Ex. if num equals 3, we get 3 * 2!, etc.
	else
		return(num*factorial(num-1));
}