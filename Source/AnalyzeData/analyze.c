#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	char filename[25] = "test.txt";
	char *buffer = 0;
	FILE *fp = fopen(filename, "rb");
	long length;

	printf("The contents of %s file are:\n", filename);
	if (fp){
 		fseek(fp, 0, SEEK_END);
 		length = ftell (fp);
 		fseek(fp, 0, SEEK_SET);
 		buffer = malloc (length);
 		if (buffer){
			fread(buffer, 1, length, fp);
		}
  		fclose (fp);
	}
	printf("%s\n",buffer);
	printf("%lu\n",strlen(buffer));

	//1. Email address
	//2. Credit card number
	//3. Living adress and phone number
	//4. Login password
	//5. Server protocol password
}