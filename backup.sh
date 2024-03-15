#!/bin/bash

# Define source, destination, and backup directories
local_directory="/data/pnoi-corpus_etl"
remote_directory="/home/wtc14/jeevan/data-corpus/"
backup_directory="pnoi-corpus_etl/backup"

# Set dry_run to true for a trial run without making any changes
dry_run=false

# Rsync command
rsync_options=(-avz --backup --backup-dir="$backup_directory" --delete)

# Add --dry-run option if dry_run is true
[ "$dry_run" = true ] && rsync_options+=(--dry-run)

# Append source and destination directories
rsync "${rsync_options[@]}" "$local_directory" "$remote_directory"