# How to run
    In the current directory, run "make", and there should be a exec file calls "analyze".
    Run "./analyze" to get the output file.
    The input file is currently "test.txt", the output file will be "output_data.txt", wrote down the information we want from the keylog.

# Rules for analyzing data we got using keylogger
### 1. Check for user's email adresses:
    the following might be the password.
    ** using namchen@ucdavis.edu for test now

### 2. Search for a string of 16 digits followed by 4 digits, and then 3 or 4 digits:
    this is the ragular patern of a credit card.

### 3. Search for state name('CAPITALed' ca/ny/..... ) followed by 5 digits:
    strings ahead might contain living address and phone number.

### 4. Check the timestamp:
    if a repeated string is typed after a long time gap, this might be the password for the device.

### 5. Search for 'ssh' 'xxxxxxxx' following a 'enter'
    the next string will be the password to the server, and 'xxxxxxx' will be recorded to find the username.
    ** also needs to work with sftp/ ftp/ telnet, but only using ssh for testing now

## ps. need to do process with 'enter' 'space' and 'capital'. Currently finished 1/2/5, working on 3/4