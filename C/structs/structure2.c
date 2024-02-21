/*
	Name: Michael Welford
	File Name: structure2.c
*/
#include <stdio.h>
#include <string.h>

// Create a struct that contains an integer called num and a string (char*) called kind.
struct cheese
{
	int num;
	char* kind[30];

};

// A further example of using structs.
int main()
{
	// Create an example of a struct and print its values.
	struct cheese a = {20,"Good"};
	printf("A has a number %i and a kind %s.",a.num, a.kind);
	return 0;
}
