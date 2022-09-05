#file: roasacomms
#rosacomms parameter-completion

function _roscomplete_rosacomms(){
    local arg opts
    COMPREPLY=()
    arg="${COMP_WORDS[COMP_CWORD]}" #get argument at position COMP_CWORD ()

    if [[ $COMP_CWORD == 1 ]]; then
            opts="pub"
            COMPREPLY=($(compgen -W "$opts" -- ${arg})) 
    else [[ ${COMP_WORDS[1]} == "pub" ]]
        local topic_pos type_pos msg_pos
        topic_pos=2
        type_pos=3
        msg_pos=4
        if [[ $COMP_CWORD == $topic_pos ]]; then
                opts=$(rostopic list 2> /dev/null)
                COMPREPLY=($(compgen -W "$opts" -- ${arg}))
        elif [[ $COMP_CWORD == $type_pos ]]; then
                opts=$(rostopic info ${COMP_WORDS[$COMP_CWORD-1]} 2> /dev/null | awk '/Type:/{print $2}')
                #if [-z "$opts"]; then
                #        opts=$(_msg_opts ${COMP_WORDS[$COMP_CWORD]})
                #fi
                COMPREPLY=($(compgen -W "$opts" -- ${arg}))
        elif [[ $COMP_CWORD == $msg_pos ]]; then
                opts=$(rosmsg-proto msg 2> /dev/null -s ${COMP_WORDS[COMP_CWORD-1]})
                if [ 0 -eq $? ]; then
                        COMPREPLY="$opts"
                fi
        fi
    fi       
}

complete -F "_roscomplete_rosacomms" "rosacomms"