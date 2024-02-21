/*
	Name: Michael Welford
	File Name: loops.c
*/
#include <stdio.h>

// A short program to work with loops.
int main()
{
	// Declare and initialize the value of a.
	int a = 1;
	
	// An example of a while loop.
	// While a is less than or equal to 6:
	while(a <= 6)
	{
		// Print a and increment it.
		printf("%d",a);
		a++;
	}
	
	printf("\n");
	
	// An example of a do while loop.
	do
	{
		// Print the value of a and increment it by 1.
		printf("%d",a);
		a++;
		
		// An example of a break statement.
		if (a == 9) 
			break; // This breaks the loop before printf(a=9).
		
	}while(a <=10); // while a is less than or equal to 10.
	printf("\n");
	
	// An example for loop.
	// For a from 1 while a is less than 11, increment by 1.
	for (a = 1; a < 11; a++) // prints 1-10 * 10 times
	{
		// For i from 0 while i is less than 10, increment by 1.
		for (int i = 0; i < 10; i++)
			// Print the value of a.
			printf("%d\n",a);
	}
	
	// End the program.
	return 0;
}