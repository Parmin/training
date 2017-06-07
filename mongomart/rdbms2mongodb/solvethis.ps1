# PowerShell

# This script is used to set your workspace to a given solution.
# That allows to verify a solution, or to have a clean starting
# point for the next exercise

# Run with:
#
#  powershell -executionpolicy bypass -file .\solvethis.ps1

$folder_solutions="solutions"
$ws="java"
$revert=0
$_positionals=@()
$_required_args_string="'<lab>'"
$backup_folder="./.backup"

function die($message, $ret) {
	$_ret=$ret
	if ( ! $_ret ) {
	$_ret=1
  }
	if ( $_PRINT_HELP -eq 'yes' ) {
		 print_help
	}
	Write-Error $message
  [Environment]::Exit(${_ret})
}

function print_help() {
	$script_name = Split-Path -leaf $PSCommandPath
	echo "solvethis.sh usage - this script will only run from within the workshop folder"
	printf 'Usage: %s [-r|--revert] [-h|--help] <lab>\n' "$script_name"
	printf "\t%s\n" "<lab>: lab to be solved"
	printf "\t%s\n" "-r,--revert: reverts to workspace before applied solution"
}

function create_backup($source) {
	Remove-Item $backup_folder
	New-Item -ItemType Directory -path $backup_folder
  copy_files $source $backup_folder
}

function copy_files($source, $target) {
	# check if destination folder exists
	if ( !(Test-Path -Path $target) ) {
		die "Not possible to apply '$source' into folder '$target' since '$target' does not exist"
	}

	if ( !(Test-Path -Path $source) ) {
		die "Not possible to apply '$source' into folder '$target' since '$source' does not exist"
	}
	# copy files recursively
  Copy-Item -path $source/* -destination $target -Recurse
}

function apply_solution() {
	if ( !(Test-Path -Path $folder_solutions) ) {
		$current_dir = $(get-location)
		die "No solutions folder found in the current local folder: $current_dir"
	}

  $solution="./$folder_solutions/$lab"

  if ( Test-Path -Path $solution ) {
    # create a backup folder
    create_backup $ws
		# apply solution
    copy_files $solution $ws
  } else {
    echo "Could not find the '$lab' solution that you are looking for"
    echo "These are the available solutions:"
    ((Gci $solutions | sort-object name)).fullname
  }
}

function revert() {
  if ( Test-Path -Path $backup_folder ) {
		Remove-Item $ws/*
    copy_files $backup_folder $ws
  } else {
    die "Nothing to backup from! $backup_folder is empty"
  }
}

foreach ( $_key in $args ) {
	switch -regex ( $_key ) {
		"-r.*|--revert" {
			$revert=1
		}
		"-h.*|--help" {
			print_help
			[Environment]::Exit(0)
		}
		default {
			$_positionals += $_key
		}
	}
}

if ( $positionals.Length -lt 1 ) {
  $_PRINT_HELP=yes
	die "FATAL ERROR: Not enough positional arguments - we require exactly 1 (namely: $_required_args_string), but got only ${#_positionals[@]}." 1
}

if ( $positionals.Length -gt 1 ) {
	$_PRINT_HELP=yes
	die "FATAL ERROR: There were extra positional arguments --- we expect exactly 1 (namely: $_required_args_string), but got ${#_positionals[@]} (the last one was: '${_positionals[*]: -1}')." 1
}

$lab=$_positionals[0]

if ( $revert -eq 1 ) {
	echo "Reverting to last known backup"
  revert
} else {
	echo "Applying solution from lab: $lab"
  apply_solution
}
