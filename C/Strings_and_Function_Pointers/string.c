/*
	Name: Michael Welford
	File Name: string.c
*/
#include <stdio.h>
#include <string.h>

int main()
{
	// Basics
	char str1[] = "Hello";
	char str2[] = {'H','e','l','l','o','\0'};
	char str3[20];
	
	
	printf("%s\n",str2);
	printf("%c\n",(strcmp(str1,str2)));
	printf("%d\n",strlen(str1));
	printf("%s\n",strlwr(str1));
	printf("%s\n",strupr(str1));
	printf("%s\n",strrev(str1));
	strcpy(str3,str1);
	strcat(str3,str2);
	printf("%s\n",str3);
	
	// String input
	char first_name[25];
	int age;
	printf("Enter your first name and age: \n");
	scanf("%s %d", first_name, &age);
	getchar(); // Needed to absorb \n character.
	
	printf("Hello %s, you are %d years old.",first_name, age);
	
	char full_name[50];
	printf("\nEnter you full name: ");
	gets(full_name);
	printf("Hello %s.",full_name);
	
	printf("\nEnter you name again: ");
	fgets(full_name,50,stdin); // fgets(string_name,string_length,input_pointer)
	printf("Hello %s",full_name);
	
	// String output
	
	fputs(full_name,stdout); // the second argument is a pointer telling where to output
	puts(full_name);
	
	return 0;
}