# Linux Homework Tasks

This folder contains my notes and practice commands for the Linux homework. Commands marked with `sudo` need administrator permission. I used harmless files and a test account so the exercises do not affect real data or users.

## Task 1: Soft Links and Hard Links

A **link** is another directory entry that gives access to a file.

| Feature | Soft link (symbolic link) | Hard link |
| --- | --- | --- |
| Points to | A path/name of another file | The same inode (file data) |
| Can cross file systems | Yes | No |
| Can link directories | Usually yes | Normally disallowed for users |
| If original is deleted | Becomes a broken/dangling link | Still accesses the file data |
| `ls -l` display | `link -> target` | Same inode as the original |

### Commands used

`ln -s TARGET LINK_NAME` creates a soft link.  
`ln TARGET LINK_NAME` creates a hard link.  
`rm LINK_NAME` deletes a link name; it does not delete the target when removing a symbolic link.

### Safe practice

Run these commands in a temporary directory:

```bash
mkdir -p ~/linux-link-practice
cd ~/linux-link-practice
printf 'Linux link practice\n' > original.txt

# Create links
ln -s original.txt soft-link.txt
ln original.txt hard-link.txt

# Inspect names, inode numbers, and contents
ls -li original.txt soft-link.txt hard-link.txt
cat soft-link.txt
cat hard-link.txt

# Delete only the soft-link directory entry
rm soft-link.txt
ls -l original.txt hard-link.txt

# The hard link still works after deleting the original name
rm original.txt
cat hard-link.txt

# Clean up the remaining hard link
rm hard-link.txt
cd ..
rmdir ~/linux-link-practice
```

`ls -li` shows that `original.txt` and `hard-link.txt` have the same inode number. A symbolic link has its own inode and stores the target path. File data is finally removed only when its hard-link count reaches zero.

### Interview answer

> A symbolic link is a separate file that stores a path to its target, so it can cross file systems but breaks if the target path disappears. A hard link is another name for the same inode and data, so deleting one name does not remove the data while another hard link exists. Hard links generally cannot span file systems or be made to directories.

## Task 2: `adduser` vs `useradd`

`useradd` is the low-level, standard account-creation utility. Its behavior is controlled by `/etc/default/useradd` and `/etc/login.defs`; options must usually be provided explicitly.

On Debian and Ubuntu, `adduser` is a friendly Perl wrapper around `useradd`. It is interactive and normally creates a home directory, asks for account details/password, and applies local defaults. For an administrator creating a regular interactive account on Ubuntu, `adduser` is generally preferred because it is safer and easier. In automation, `useradd` is common because its options are explicit and non-interactive.

> Note: command availability and defaults vary by distribution. For example, some non-Debian distributions provide `adduser` as a direct alias or package. Check with `man adduser` and `man useradd` on the target host.

### Create and verify a test user (Ubuntu/Debian)

Choose a name that does not already exist, then run:

```bash
sudo adduser linuxpractice
id linuxpractice
getent passwd linuxpractice
ls -ld /home/linuxpractice
```

`id` displays the user and group IDs. `getent passwd` verifies the account through the system name-service configuration. The home-directory listing verifies that it was created.

### Remove the test account after practice

Only run this when `linuxpractice` is the disposable test user created above:

```bash
sudo deluser --remove-home linuxpractice
```

Do not use a real person's account as a test account.

## Task 3: `journalctl`

`journalctl` reads logs collected by **systemd-journald**. It is used to investigate boot problems, kernel messages, service failures, authentication-related events, and application output from systemd services. Some distributions use traditional text logs as well; the journal may be non-persistent unless configured to store logs under `/var/log/journal`.

### Useful commands

```bash
# View the journal (use sudo when permission is denied)
journalctl

# View logs from the current boot; previous boot is -b -1
journalctl -b
journalctl -b -1

# Show the most recent entries and follow new ones live
journalctl -n 50
journalctl -f

# Filter by time and show readable timestamps
journalctl --since 'today' --output short-iso
journalctl --since '2026-09-03 09:00' --until '2026-09-03 10:00'

# View kernel messages
journalctl -k -b
```

### Check one service

Replace `ssh` with a service installed on the machine. Ubuntu commonly uses `ssh.service` when the OpenSSH server is installed:

```bash
sudo systemctl status ssh.service
sudo journalctl -u ssh.service -b --no-pager
sudo journalctl -u ssh.service -n 50 --no-pager
sudo journalctl -u ssh.service -f
```

`-u` filters by systemd unit, `-b` limits output to the current boot, and `-f` follows new entries. First use `systemctl list-units --type=service` if unsure of the exact unit name.

## Task 4: Linux Command Cheat Sheet

This compact cheat sheet covers important everyday commands. Read the manual for details: `man COMMAND`, or use `COMMAND --help`.

| Command | Purpose | Basic example |
| --- | --- | --- |
| `pwd` | Print current directory | `pwd` |
| `ls` | List files | `ls -lah` |
| `cd` | Change directory | `cd /var/log` |
| `mkdir` | Create directory | `mkdir -p projects/linux` |
| `touch` | Create/update empty file | `touch notes.txt` |
| `cp` | Copy files/directories | `cp source.txt copy.txt` |
| `mv` | Move or rename | `mv old.txt new.txt` |
| `rm` | Remove files | `rm unwanted.txt` |
| `rmdir` | Remove empty directory | `rmdir empty-dir` |
| `cat` | Print file content | `cat notes.txt` |
| `less` | Read a file page by page | `less /var/log/syslog` |
| `head` / `tail` | Show beginning/end of file | `tail -n 20 app.log` |
| `grep` | Search text | `grep -n 'error' app.log` |
| `find` | Locate files by criteria | `find . -name '*.log'` |
| `wc` | Count lines/words/bytes | `wc -l notes.txt` |
| `sort` / `uniq` | Sort and deduplicate | `sort names.txt \| uniq` |
| `chmod` | Change permissions | `chmod u+x script.sh` |
| `chown` | Change file owner | `sudo chown user:group file` |
| `ps` | Show processes | `ps aux` |
| `top` | Interactive process monitor | `top` |
| `kill` | Send a signal to a process | `kill PID` |
| `df` | Show filesystem free space | `df -h` |
| `du` | Show directory/file size | `du -sh directory` |
| `free` | Show memory usage | `free -h` |
| `whoami` / `id` | Show current identity/IDs | `id` |
| `sudo` | Run an authorized command as administrator | `sudo systemctl status ssh` |
| `systemctl` | Control/inspect systemd units | `systemctl status ssh.service` |
| `journalctl` | Query systemd journal logs | `journalctl -u ssh.service` |
| `tar` | Create/extract archives | `tar -czf backup.tar.gz directory/` |
| `ssh` | Remote shell connection | `ssh user@host` |
| `scp` | Copy files over SSH | `scp file.txt user@host:/tmp/` |

### Practice routine

```bash
mkdir -p ~/linux-command-practice
cd ~/linux-command-practice
printf 'banana\napple\nbanana\n' > fruit.txt
ls -lah
cat fruit.txt
grep -n banana fruit.txt
sort fruit.txt | uniq
wc -l fruit.txt
find . -type f
du -sh .
df -h .
```

Be careful with `sudo`, `rm`, `chown`, and permission changes. Before deleting or changing ownership, confirm the path with `pwd` and `ls`.

## What I completed

- Documented the distinction, creation, inspection, and safe deletion of symbolic and hard links.
- Documented why `adduser` is the recommended interactive choice on Ubuntu and included a test-user workflow.
- Documented `journalctl` usage and service-log investigation commands.
- Added a practical Linux command reference and a small, non-destructive exercise.
