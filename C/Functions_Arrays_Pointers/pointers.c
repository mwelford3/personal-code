/*
	Name: Michael Welford
	File Name: pointers.c
*/
#include <stdio.h>

// Declare a function that accepts a pointer to an integer.
void test(int *num);

// A program to practice using pointers.
int main()
{
	int a = 5;
	int *b = NULL;
	b = &a;
	printf("The address of a is %x\n",&a);
	printf("b points to a at %x\n",b);
	
	*b = 2;
	printf("The address of a is %x\n",&a);
	printf("b points to a with a value of %d\n",*b);
	
	// Shows an example of using pointers with arrays.
	int c[3] = {1,2,3};
	int *d = c;
	for (int i = 0; i < 3; i++)
	{
		printf("%d ",*(d+i));
	}
	printf("\n");
	
	d++;
	printf("%d\n", *d);
	
	
	// functions with pointers "Pass by Address"
	int e = 2;
	test(&e);
	printf("%d\n",e);
	return 0;
}

// A function that sets the value num points to to 3.
void test(int *num)
{
	*num = 3;
}