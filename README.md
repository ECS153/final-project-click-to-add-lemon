# final-project-click-to-add-lemon
## Keylogger
## Computer Security ECS 153 project

### Structure
Within the Source directory, we have our keylog.c file which is the keylogger which can be installed into the linux kernel. Then, we have several directories for the other tools surrounding the keylogger. The PhishingApplication directory contains the source code and binary for the CurrencyConverter which serves to fool the user and install the keylogger into the system. The Analysis directory contains the tool to filter out useless keystrokes and obtain useful information from the keylogged files. The Scripts directory contains the user script which encrypts and sends images to twitter whereas the server script fetches images from twitter and decrypts. 

These tools are automated by the phishing application, so all that needs to be done is to run the phishing application and give it your admin password. Then scripts will automatically run the analysis, encryption, and twitter posting parts periodically.

### Keylog and Class Concepts
The keylogger is installed in the kernel level, which makes it harder to detect and has more control over the higher layers in the system (i.e. user application layer). 

