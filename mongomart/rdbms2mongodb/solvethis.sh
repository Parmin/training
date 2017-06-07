#!/bin/sh

# This script is used to set your workspace to a given solution.
# That allows to verify a solution, or to have a clean starting
# point for the next exercise

folder_solutions="solutions"
ws="java"
revert=0
_positionals=()
_required_args_string="'<lab>'"
backup_folder="./.backup"

function die() {
	local _ret=$2
	test -n "$_ret" || _ret=1
	test "$_PRINT_HELP" = yes && print_help >&2
	echo "$1" >&2
	exit ${_ret}
}

function print_help() {
	script_name=$0
	echo "solvethis.sh usage - this script will only run from within the workshop folder"
	printf 'Usage: %s [-r|--revert] [-h|--help] <lab>\n' "$script_name"
	printf "\t%s\n" "<lab>: lab to be solved"
	printf "\t%s\n" "-r,--revert: reverts to workspace before applied solution"
}

function create_backup() {
	rm -rf $backup_folder
	mkdir -p $backup_folder
  copy_files $1 $backup_folder
}

function copy_files() {
	# check if destination folder exists
	if [ ! -d $2 ]; then
		die "Not possible to apply '$1' into folder '$2' since '$2' does not exist"
	fi

	if [ ! -d $1 ]; then
		die "Not possible to apply '$1' into folder '$2' since '$1' does not exist"
	fi
  # copy files recursively
  cp -r $1/* $2 2>/dev/null
}

function apply_solution() {
	if [ ! -d $folder_solutions ]; then
		current_dir = $(pwd)
		die "No solutions folder found in the current local folder: $current_dir"
	fi

  solution="./$folder_solutions/$lab"

  if [ -d $solution ]; then
    # create a backup folder
    create_backup $ws
		# apply solution
    copy_files $solution $ws
  else
    echo "Could not find the '$lab' solution that you are looking for"
    echo "These are the available solutions:"
    ls -1 $folder_solutions
  fi
}

function revert() {
  if [ -d $backup_folder ]; then
		rm -rf $ws/*
    copy_files $backup_folder $ws
  else
    die "Nothing to backup from! $backup_folder is empty"
  fi
}

while test $# -gt 0
do
	_key="$1"
	case "$_key" in
		-r*|--revert)
			revert=1
			;;
		-h*|--help)
			print_help
			exit 0
			;;
		*)
			_positionals+=("$1")
			;;
	esac
	shift
done

if [ ${#_positionals[@]} -lt 1 ]; then
	_PRINT_HELP=yes
	die "FATAL ERROR: Not enough positional arguments - we require exactly 1 (namely: $_required_args_string), but got only ${#_positionals[@]}." 1
fi

if [ ${#_positionals[@]} -gt 1 ]; then
	_PRINT_HELP=yes
	die "FATAL ERROR: There were extra positional arguments --- we expect exactly 1 (namely: $_required_args_string), but got ${#_positionals[@]} (the last one was: '${_positionals[*]: -1}')." 1
fi

lab=$_positionals

if [ $revert == 1 ]; then
	echo "Reverting to last known backup"
  revert
else
	echo "Applying solution from lab: $lab"
  apply_solution
fi
