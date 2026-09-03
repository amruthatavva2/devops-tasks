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
