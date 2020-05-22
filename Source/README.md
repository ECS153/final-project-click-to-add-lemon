# Instructions on running the keylogger manually

With the new update no hardcoded memory is needed

Run makefile.

`$ make`

Then, you'll get keylog.ko file. Insert the module into the kernel.

`$ sudo insmod keylog.ko`

You can double check to see if the kernel was loaded properly by checking if there is "keylog" inside:

`$ lsmod`

Printk messages from the code can be seen with (Printf is not available for kernel modules):

`$ dmesg`

Keylogger module can be removed with:

`$ sudo rmmod keylog`

To see the logged file 
`sudo cat /proc/buffer_file`