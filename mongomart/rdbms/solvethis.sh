#!/bin/sh
# This script is meant to be used by students so they don't get stuck in
# particular exercise.

folder_solutions="solutions"
ws="java"
revert=0
_positionals=()
_required_args_string="'<lab>'"
backup_folder=./.backup

die()
{
	local _ret=$2
	test -n "$_ret" || _ret=1
	test "$_PRINT_HELP" = yes && print_help >&2
	echo "$1" >&2
	exit ${_ret}
}


print_help ()
{
	echo "solvethis.sh usage - this script will only run from within the workshop folder"
	printf 'Usage: %s [-r|--revert] [-h|--help] <lab>\n' "$0"
	printf "\t%s\n" "<lab>: lab to be solved"
	printf "\t%s\n" "-r,--revert: reverts to workspace before applied solution"
}


function create_backup(){
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

  cp -r $1/* $2/. 2>/dev/null
}

function apply_solution(){

	if [ ! -d $folder_solutions ]; then
		die "No solutions folder found in the current local folder: $(pwd)"
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
    ls -R $folder_solutions | cat
  fi
}

function revert(){
  if [ -d $backup_folder ]; then
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

test ${#_positionals[@]} -lt 1 && _PRINT_HELP=yes die "FATAL ERROR: Not enough positional arguments - we require exactly 1 (namely: $_required_args_string), but got only ${#_positionals[@]}." 1
test ${#_positionals[@]} -gt 1 && _PRINT_HELP=yes die "FATAL ERROR: There were spurious positional arguments --- we expect exactly 1 (namely: $_required_args_string), but got ${#_positionals[@]} (the last one was: '${_positionals[*]: -1}')." 1

lab=$_positionals


if [ $revert == 1 ]; then
  revert
else
  apply_solution
fi
