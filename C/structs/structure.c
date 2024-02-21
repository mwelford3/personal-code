/*
	Name: Michael Welford
	File Name: structure.c
*/
#include <stdio.h>

// An example of a structure in c.
// This one contains an integer number and char grade.
struct apple
{
	int number;
	char grade;
};

// An example program for using structs.
int main()
{
	// Create an example struct.
	struct apple a = {1,'A'};
	
	// Print the number of apple.
	printf("%i",a.number);

	return 0;
}
