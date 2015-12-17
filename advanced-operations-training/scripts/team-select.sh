#!/bin/bash

valid_team_names=(
    team01
    team02
    team03
    team04
    team05
)

function contains() {
    local n=$#
    local value=${!n}
    for ((i=1;i < $#;i++)) {
        if [ "${!i}" == "${value}" ]; then
            return 0
        fi
    }
    return 1
}


function main() {
    if [ "$(whoami)" != root ]
    then
        echo >&2 'This script must run as root'
        exit 1
    fi

    if [ $# != 1 ]
    then
        echo >&2 'Usage: team-select.sh <team-name>'
        exit 1
    fi
    local selected_team="$1"
    echo 'Selecting team:' "$selected_team"

    if ! contains "${valid_team_names[@]}" "$selected_team"
    then
        echo >&2 'Not a valid team name:' "$selected_team"
        echo >&2 'Valid team names are:' "${valid_team_names[@]}"
        exit 1
    fi

    # comment all mmsGroupId and mmsApiKey lines
    # uncomment selected_team's section
    sed -i /etc/mongodb-mms/automation-agent.config \
        -e '/mmsGroupId/ s/^[# ]*/# /' \
        -e '/mmsApiKey/  s/^[# ]*/# /' \
        -e "/$selected_team/,+2 { /$selected_team/b; s/^[# ]*// }"
    # restart the agent to pick up the new config
    service mongodb-mms-automation-agent restart

    # edit the bash prompt
    su ec2-user <<SU_EC2_USER
        sed -i /home/ec2-user/.bashrc \
            -e '/^TEAM=/ s/^.*$/TEAM=$selected_team/'
SU_EC2_USER
}

main "$@"
