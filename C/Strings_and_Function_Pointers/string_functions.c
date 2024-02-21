/*
	Name: Michael Welford
	File Name: string_functions.c
*/
#include <stdio.h>

// A program to practice string functions.
int main()
{
	// sprintf -> makes a formatted string from given values
	char info[100];
	char dept[] = "HR";
	int emp = 75;
	sprintf(info,"The %s dept has %d employees.", dept, emp);
	printf("%s\n",info);
	
	// sscanf -> makes a formatted string from read values
	char info2[] = "Rockford IL 13190";
	char city[50];
	char state[50];
	int population;
	sscanf(info2," %s %s %d", city, state, &population);
	printf("%d people live in %s, %s.", population, city, state);
	
	return 0;
}