#!/bin/bash
# Agent Cellphone V2 - Messaging CLI Bash/Zsh Completion
# Source this file in your shell: source scripts/messaging_cli_completion.sh
#
# IMPORTANT: Regular priority is the DEFAULT - no --priority flag needed!
# Only use --priority urgent or --high-priority for true emergencies

_messaging_cli_complete() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # All available options
    opts="--message --sender --agent --bulk --type --priority --high-priority --mode --no-paste --new-tab-method --list-agents --coordinates --history --check-status --queue-stats --process-queue --start-queue-processor --stop-queue-processor --onboarding --onboard --onboarding-style --get-next-task --wrapup --help"

    # Short options
    opts="$opts -m -s -a -t -p"

    case "${prev}" in
        # Options that take specific values
        --agent|-a)
            # List available agents (you could dynamically generate this)
            COMPREPLY=( $(compgen -W "Agent-1 Agent-2 Agent-3 Agent-5 Agent-6 Agent-7 Agent-8 Agent-4" -- "${cur}") )
            return 0
            ;;
        --sender|-s)
            # Common sender options
            COMPREPLY=( $(compgen -W "Captain Agent-4 System Admin" -- "${cur}") )
            return 0
            ;;
        --type|-t)
            COMPREPLY=( $(compgen -W "text broadcast onboarding" -- "${cur}") )
            return 0
            ;;
        --priority|-p)
            COMPREPLY=( $(compgen -W "regular urgent" -- "${cur}") )
            return 0
            ;;
        --mode)
            COMPREPLY=( $(compgen -W "pyautogui inbox" -- "${cur}") )
            return 0
            ;;
        --new-tab-method)
            COMPREPLY=( $(compgen -W "ctrl_t ctrl_n" -- "${cur}") )
            return 0
            ;;
        --onboarding-style)
            COMPREPLY=( $(compgen -W "friendly professional" -- "${cur}") )
            return 0
            ;;
        --message|-m)
            # Don't complete message content
            return 0
            ;;
        *)
            ;;
    esac

    # Filter options based on what's already been used
    local used_opts=""
    for word in "${COMP_WORDS[@]}"; do
        case "$word" in
            --agent|--bulk|--onboarding|--wrapup|--list-agents|--coordinates|--history|--check-status|--queue-stats|--process-queue|--start-queue-processor|--stop-queue-processor|--get-next-task|--onboard)
                used_opts="$used_opts $word"
                ;;
        esac
    done

    # Remove already used options from completion
    for used in $used_opts; do
        opts=$(echo "$opts" | sed "s/\b$used\b//g")
    done

    # Generate completions
    COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )

    # If no matches, try partial matches
    if [ ${#COMPREPLY[@]} -eq 0 ]; then
        COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )
    fi

    return 0
}

# Register completion function
if [ -n "$ZSH_VERSION" ]; then
    # Zsh completion
    autoload -U compinit && compinit
    autoload -U bashcompinit && bashcompinit
fi

complete -F _messaging_cli_complete messaging_cli
complete -F _messaging_cli_complete python

# Optional: Complete for different ways to run the CLI
complete -F _messaging_cli_complete "python -m src.services.messaging_cli"

echo "✅ Messaging CLI completion loaded!"
echo "   Try: messaging_cli --<TAB>"
echo "   Or:  python -m src.services.messaging_cli --<TAB>"
