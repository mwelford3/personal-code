/*
  Name: Michael Welford
  File Name: condition.c
*/

#include <stdio.h>

// A short program that uses conditional statements.
int main()
{
	// Input a basic integer from stdin. 
	int a;
	printf("Input an integer: ");
	scanf("%d",&a);
	
	// Define some integer variables.
	int b = 3;
	int c;
	int d;
	
	// Can also do nested if statements
	// If b is less than a:
	if (b < a)
	{
		// If a is equal to two more than b.
		if(a == b+2)
			printf("Good.\n");
		// Otherwise:
		else
			printf("Yes.\n");
	}
	// Else if a is equal to 1:
	else if (a == 1)
	{
		printf("It's 1.\n");
	}
	// Else:
	else
	{
		printf("No.\n");
	}
	
	// An example of using the conditional operator.
	// If b > a set c to 1, else set it to 0. Then, print c.
	c = (b > a)? 1:0;
	printf("%d\n",c);
	
	// Input a integer value for d.
	printf("Input a value for d: ");
	scanf("%d",&d);
	
	// Check the value for d in each case
	// and then print the value depending on its value.
	switch (d){
		case 1:
			printf("d is 1\n");
			break;
		case 2: 
			printf("d is 2\n");
			break;
		case 3:
			printf("d is 3\n");
			break;
		default:
			printf("%d\n",d);
			break;
	}
	
	// End the program.
	return 0;
}