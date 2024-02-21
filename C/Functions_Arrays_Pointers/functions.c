/*
	Name: Michael Welford
	File Name: functions.c
*/
#include <stdio.h>

// Declare functions.
int square(int); // Ex. square is a function that takes an int and returns an int.
void happy(); // happy is a function that takes nothing and returns nothing.
void numPrint(int, int);
void repeatHello();

// A program to practice using functions.
int main()
{
	int a = 2;
	printf("%d\n",square(a));
	happy();
	numPrint(3,4);
	
	for(int i = 0; i < 5; i++)
	{
		repeatHello();
	}
	return 0;
}

/***
 A function that returns the square of a number.
 Parameters: x - the integer to be squared
 Returns: x*x - the integer square of x.
***/
int square(int x)
{
	return x*x;
}

/***
 A simple void function example.
***/
void happy()
{
	printf("Happy!\n");
}

/***
 A function that prints all the integers between start and start+number
 
 Parameters: start - the starting integer value
             number - the number of times to increment start
 Returns: void
***/
void numPrint(int start, int number)
{
	int num = start;
	for (int i = 0; i < number; i++)
	{
		printf("%d\n",num);
		num++;
	}
}

/***
 A function to practice using static variables.
 Prints and increments the static variable.
***/
void repeatHello()
{
	static int num_calls = 1;
	
	printf("Hello number %d\n", num_calls);
	num_calls++;
	
}