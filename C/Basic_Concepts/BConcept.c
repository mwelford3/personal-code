/*
    Name: Michael Welford
	File: BConcept.c
*/
#include <stdio.h>

#define PI 3.14

// An example of printing in c.
int main()
{
	// This is a comment
	/* This is a body comment. */
	
	// Basic data types.
	int a; // integer
	char b; // character
	char c[100]; //string as an array of char
	float d; // float
	
	// Printing integers.
	// Print a prompt.
	printf("Input a value: ");
	// Input a number into a as an int.
	scanf("%4d",&a);
	// Print a.
	printf("%d\n",a);
	// Print the size of an integer.
	printf("%d\n",sizeof(int));
	
	//Printing characters.
	// Print a prompt.
	printf("Input a character: ");
	//Input a char into b.
	scanf(" ");
	scanf("%1c",&b);
	//Print b.
	printf("%c\n",b);
	
	// An example of printing Pi.
	printf("%0.2f",PI);
	
	// Printing strings.
	// Get another character.
	printf("\nInput a string: ");
	scanf(" ");
	// Get the string. 
	gets(c);
	// Print the string.
	printf("The constant is %s.\n",c);
	
	// Similarly input and print a double.
	printf("Input a double: ");
	scanf("%10f",&d);
	printf("%0.0f",d);
	return 0;
}