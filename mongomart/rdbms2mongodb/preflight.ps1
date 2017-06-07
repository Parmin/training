# PowerShell

# This script will run system requirement checks for the rdbms2mongodb lab

# Run with:
#
#  powershell -executionpolicy bypass -file .\preflight.ps1

$expected_mysqlversion="5.7"
$expected_mongodb="v3.4"
$expected_java="1.8"
$expected_maven="3.5"

$SOMETHING_MISSING=0

function print_good($message) {
   write-host $message -foregroundcolor green
}

function print_error($message) {
  write-host $message -foregroundcolor red
  $SOMETHING_MISSING=1
}

function check_version($cmd, $expected) {
  $out = & "$cmd" --version 2>&1
  $outs = $out[0] -split " "
  $version = $outs[2]
  if ( -NOT $version.StartsWith($expected) )
  {
    print_error "Your current version $version is not the expected: $expected"
  } else {
    print_good "Correct version found: $version"
  }
}

function check_mysql_version($cmd, $expected) {
  $out = & "$cmd" --version 2>&1
  $out -match " Ver\s+(\S+)"
  $version = $matches[1]
  if ( -NOT $version.StartsWith($expected) )
  {
    print_error "Your current version $version is not the expected: $expected"
  } else {
    print_good "Correct version found: $version"
  }
}

function check_java_version($cmd, $expected) {
  $out = & "$cmd" -version 2>&1
  $outs = $out[0] -split " "
  $version = $outs[2]
  if ( -NOT $version.StartsWith('"' + $expected) )
  {
    print_error "Your current version $version is not the expected: $expected"
  } else {
    print_good "Correct version found: $version"
  }
}

function check_mysql {
  echo "Check for MySQL installation and version: $expected_mysqlversion"
  $mysqld_exec=(Get-Command mysqld).Path
  if ( $mysqld_exec )
  {
    print_good "MySQL installed: $mysqld_exec"
    check_mysql_version $mysqld_exec $expected_mysqlversion
  } else {
    print_error "mysqld could not be found!"
  }
}

function check_mongodb {
  echo "Check for MongoDB installation and version: $expected_mongodb"
  $mongod_exec=(Get-Command mongod).Path
  if ( $mongod_exec )
  {
    print_good "MongoDB installed: $mongod_exec"
    check_version $mongod_exec $expected_mongodb
  } else {
    print_error "mongod could not be found!"
  }
}

function check_java {
  echo "Check for Java installation and version: $expected_java"
  $jexec=(Get-Command java).Path
  if ( $jexec )
  {
    print_good "Java installed: $jexec"
    check_java_version $jexec $expected_java
  } else {
    print_error "java could not be found!"
  }
}

function check_maven {
  echo "Check for Maven installation and version: $expected_maven"
  $m_exec=(Get-Command mvn).Path
  if ( $m_exec )
  {
    print_good "Maven installed: $m_exec"
    check_version $m_exec $expected_maven
  } else {
    print_error "mvn could not be found!"
  }
}

check_mongodb
check_mysql
check_java
check_maven

if ( $SOMETHING_MISSING -ne 0 )
{
  print_error "Check your setup! Something seems to be missing."
}

exit $SOMETHING_MISSING
