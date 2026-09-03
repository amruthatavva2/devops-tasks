# Shell Scripting Homework: System Information Script

## What I did

I created a Bash system-information script. It asks the user for a directory name, creates that directory, creates a text file inside it, displays system information, and saves the current running-process list in the text file.

The complete script is included below so this README can be submitted on its own.

## Complete script: `system_info.sh`

```bash
#!/usr/bin/env bash

# System Information Script
# Creates a user-named directory and saves the current process list inside it.

set -euo pipefail

current_date=$(date)
host_name=$(hostname)
user_name=$(whoami)

read -r -p "Enter a directory name for this report: " report_directory

if [[ -z "$report_directory" ]]; then
  echo "A directory name is required."
  exit 1
fi

process_file="$report_directory/running_processes.txt"

mkdir -p "$report_directory"
touch "$process_file"

echo "=============================="
echo "System Information"
echo "=============================="
echo "Current date: $current_date"
echo "Hostname: $host_name"
echo "Username: $user_name"
echo
echo "Disk usage:"
df -h
echo
echo "Running processes:"
ps aux

# The > operator overwrites the report with the current process list.
ps aux > "$process_file"

echo
echo "Running processes saved to: $process_file"
```

## Run the script

On Linux/Ubuntu, open a terminal in this folder and run:

```bash
chmod +x system_info.sh
./system_info.sh
```

When prompted, enter a directory name such as `system-report`. The script creates `system-report/running_processes.txt` and saves the process list there. Running it again with the same directory name overwrites that process report with the latest result.

## Commands and requirements used

| Requirement | Use in `system_info.sh` |
| --- | --- |
| Variables | `current_date`, `host_name`, `user_name`, `report_directory`, and `process_file` store values. |
| `read -p` | `read -r -p` asks the user for a directory name. |
| `mkdir` | `mkdir -p "$report_directory"` creates the requested directory. |
| `touch` | `touch "$process_file"` creates the output file. |
| `echo` | Prints headings, system information, and confirmation. |
| `df` | `df -h` shows human-readable disk usage. |
| `ps` | `ps aux` displays running processes. |
| `>` redirection | `ps aux > "$process_file"` saves process information in the file. |

## How the script works

1. `date`, `hostname`, and `whoami` collect the current date, computer hostname, and logged-in username. Their results are stored in variables.
2. `read -r -p` asks the user for the directory in which to create the report.
3. `mkdir -p` creates that directory, and `touch` creates `running_processes.txt` inside it.
4. `echo` prints headings and the information stored in the variables.
5. `df -h` prints disk usage in a readable format.
6. `ps aux` prints all running processes in the terminal.
7. `ps aux > "$process_file"` writes the same running-process information into `running_processes.txt`. The `>` symbol replaces the previous file contents each time the script runs.

## Example output

Actual values and process IDs will vary by computer.

```text
Enter a directory name for this report: system-report
==============================
System Information
==============================
Current date: Wed Sep  3 10:30:00 IST 2026
Hostname: ubuntu-lab
Username: student

Disk usage:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   12G   36G  25% /

Running processes:
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
student     1234  0.0  0.1  12345  6789 pts/0    Ss   10:29   0:00 bash

Running processes saved to: system-report/running_processes.txt
```

To view the saved process report:

```bash
cat system-report/running_processes.txt
```
