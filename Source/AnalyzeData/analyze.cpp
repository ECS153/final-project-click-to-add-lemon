#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <sstream> 
#include <vector>
#include <list>

using namespace std;

char numarr[] = {
	'0',
	'1',
	'2',
	'3',
	'4',
	'5',
	'6',
	'7',
	'8',
	'9',
};

vector<long long> GetStringByNumArr(string str) {
	vector<long long> numlist;
	int startIndex = 0;
	while (startIndex != -1) {
		vector<char> tempnum;
		startIndex = -1;
		for (size_t i = 0; i < str.length(); i++) {
			for (size_t j = 0; j < 10; j++) {
				if (str[i] == numarr[j]) {
					startIndex = i;
					break;
				}
			}
			if (startIndex != -1) {
				tempnum.push_back(str[startIndex]);
				int tempindex = 0;
				char tempchar = str[startIndex + (tempindex += 1)];
				while (int(tempchar - 48) >= 0 && int(tempchar - 48) <= 9) {
					tempnum.push_back(tempchar);
					tempchar = str[startIndex + (tempindex += 1)];
				}
				str.erase(startIndex, tempindex);
				break;
			}
		}
		if (!tempnum.empty()) {
			//cout << "tempnum : " << string(tempnum.begin(), tempnum.end()) << endl;
			numlist.push_back(stoll(string(tempnum.begin(), tempnum.end())));
		}
	}
	return numlist;
}

int main() {
	//read in file into buffer calls "content"
	ifstream ifs("log_file.txt");
	string content((istreambuf_iterator<char>(ifs)),(istreambuf_iterator<char>()));
	ifs.close();
	
	//1. Email address
	string email = "namchen@ucdavis.edu";
	size_t found = 0;
	vector<int> foundEmailList;
	while (found != string::npos) {
		found = content.find(email, found+1);
		if (found != -1) {
			foundEmailList.push_back(found);
		} else {
			break;
		}
	}
	ofstream myfile;
	myfile.open("log_file_analyzed.txt");
	myfile << "###1:possible email address related data:\n" << endl; 
	for (int i = 0; i < foundEmailList.size(); i++) {
		myfile << content.substr(foundEmailList[i], 40) << endl;
		myfile << endl;
	}

	//2. Credit card number
	vector<long long> foundNumberList = GetStringByNumArr(content);
	// cout << foundNumberList.size() << endl;
	// cout << to_string(foundNumberList[0]).length() << endl;
	myfile << "###2:possible credit card number related data:\n" << endl; 
	for (int i = 0; i < foundNumberList.size(); i++) {
		if (to_string(foundNumberList[i]).length() == 16) {
			myfile << foundNumberList[i] << endl;
			myfile << foundNumberList[i+1] << endl;
			myfile << foundNumberList[i+2] << endl;
			myfile << endl;
		}
	}

	//3. Living adress and phone number
	//4. Login password

	//5. Server protocol password
	string protocol = "ssh";
	found = 0;
	vector<int> foundConnectionList;
	while (found != string::npos) {
		found = content.find(protocol, found+1);
		if (found != -1) {
			foundConnectionList.push_back(found);
		} else {
			break;
		}
	}
	myfile << "###5:possible connection login related data:\n" << endl; 
	for (int i = 0; i < foundConnectionList.size(); i++) {
		myfile << content.substr(foundConnectionList[i], 50) << endl;
		myfile << endl;
	}
	myfile.close();
}