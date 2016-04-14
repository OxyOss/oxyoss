#!/bin/bash
#
# Copyright (C) 2011 W. Trevor King <wking@drexel.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

# Use Monkeysphere IDs in your GnuPG keyring to identify entries in
# your known_hosts file.
#
# usage: unhash-known-hosts.sh path/to/known_hosts

KNOWN_HOSTS="~/.ssh/known_hosts"
if [ -n "${1}" ]; then
		KNOWN_HOSTS="${1}"
fi

GPG_IDS=$(gpg --list-keys ssh | grep pub | sed 's/^[^/]*\///' | sed 's/ .*//')
if [ -z "${GPG_IDS}" ]; then
		echo 'no SSH IDs found in GnuPG keyring'
		exit 1
fi

declare -A GPG_KEY
declare -A GPG_UID

for GPG_ID in $GPG_IDS; do
    GPG_ENTRY=$(gpg --export "${GPG_ID}" | openpgp2ssh)
		GPG_KEY["${GPG_ENTRY}"]="${GPG_ID}"
		GPG_UID["${GPG_ID}"]=$(gpg --list-keys "${GPG_ID}" | sed -n 's/^uid *//p')
done

while read ENTRY; do
    if [ -n "${ENTRY}" ] && [ "${ENTRY:0:1}" == "|" ]; then
				HASH=$(echo "${ENTRY}" | awk '{print $1}')
				ALG=$(echo "${ENTRY}" | awk '{print $2}')
				KEY=$(echo "${ENTRY}" | awk '{print $3}')
				#echo "${ENTRY}"
				#echo "ALG: ${ALG}"
				#echo "KEY: ${KEY}"
				ALG_KEY="${ALG} ${KEY}"
				GPG_ID="${GPG_KEY[${ALG_KEY}]}"
				if [ -n "${GPG_ID}" ]; then
						echo "GnuPG ID ${GPG_ID} (${GPG_UID[$GPG_ID]}) matches ${HASH}"
				else
						echo "did not match ${HASH}"
				fi
		fi
done < "${KNOWN_HOSTS}"

