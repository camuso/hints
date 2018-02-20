#!/bin/bash
#
# speed.sh
#
# Check for number of CPUs argument. Should only be one arg to
# this script.
#

# function usage {
#	echo
#	echo "You must provide the number of CPUs to use this script";
#	echo
#	exit
# }
#
# If we don't get exactly one argument to this script, call the
# usage function above.
#
# [ $# -eq 1 ] || usage
#
# cpu_count=$(( $1 - 1 ))

cpu_count=$(ls -d /sys/devices/system/cpu/cpu*/cpufreq | wc -l)
max_cpu=$(( cpu_count - 1 ))

echo "highest cpu: $max_cpu"
AnyKey='Press any key to continue ...'

function anykey {
	echo $1
	read -p "$AnyKey";
}

function dump_freq {
	case $1 in
		min )	arg='minumum'
				;;
		max )	arg='maximum'
				;;
		cur )	arg='current'
				;;
		* )             echo "Invalid parameter"
				usage
				;;
	esac
	anykey "Here is a list of your CPU $arg frequencies."
	cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_$1_freq
	echo
}

function set_governor {
	anykey "Setting frequency scaling governor to \"$1\"."
	for (( i = 0; i < max_cpu; i++ )); do
		#
		# Test to be sure the variable contains a number
		#
		[[ "${i//*([[:digit:]])}" ]] || continue;
		echo "$1" > /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor;
		cat /sys/devices/system/cpu/cpu$i/cpufreq/scaling_governor
	done
	echo
}

function set_speed {
	case $1 in
		min )	arg='minumum'
				;;
		max )	arg='maximum'
				;;
		* )             echo "Invalid parameter"
				usage
				;;
	esac
	anykey "Setting your CPU speeds to their $arg values"
	for (( i = 0; i < max_cpu; i++ )); do
		cat /sys/devices/system/cpu/cpu$i/cpufreq/cpuinfo_$1_freq > \
		/sys/devices/system/cpu/cpu$i/cpufreq/scaling_setspeed;
	done
	cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_cur_freq
	anykey "Listed above are the new current frequencies of your CPUs."
	echo
}

# Set cpu frequency scaling governor to "ondemand".
#
set_governor "ondemand"
dump_freq "cur"

# Set cpu frequency scaling governor to "userspace"
#
set_governor "userspace"
dump_freq "cur"

# Dump minimum frequencies and maximum frequencies.
#
dump_freq "min"
dump_freq "max"

# Set CPUs to minimum frequency
#
set_speed "min"

# Set CPUs to maximum frequency
#
set_speed "max"

# Return control to "ondemand"
#
echo
set_governor "ondemand"
dump_freq "cur"

