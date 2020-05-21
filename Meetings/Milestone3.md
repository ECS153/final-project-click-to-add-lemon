
# Meeting Notes
## Week 3 
## 05/20

[VIDEO LINK]()

### Agenda:
- Increasing scope of Kernel level keylogger
- Discussing how to load in the kernel module
- Deciding on the format of the logged keys with respect to timestamps

### Action Item:
**Hiroya:**
- Work on saving the logged keys in a file along with timestamps.
- Hide the keylogger from the user so that keylogger is harder to detect.

**Shuyao:**
- Writing bash scripts to automate the keylogger build and configuration.
- Writing bash scripts to run the keylogger, but looks innocuous.

**Marco:**
- Write code to send the logged files to the attacker's server.
- (Optional): Find libraries to deal with encrypting the files while sending.

**Nan:**
- Create key log analysis code to look at the logged files and extracting data from it using logged keys and timestamps.

