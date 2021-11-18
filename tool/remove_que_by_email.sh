#!/bin/bash
postqueue -p | grep -v '^ *(' | awk 'BEGIN { RS = "" } { if ($7 == $1) print $1 } ' | tr -d '*!' | postsuper -d -
#postqueue -p | grep -v '^ *(' | awk 'BEGIN { RS = "" } { if ($7 == "name@example.com") print $1 } ' | tr -d '*!' | postsuper -d -
#  ./remove_que_by_email.sh user@example.com
