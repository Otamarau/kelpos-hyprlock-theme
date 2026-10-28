#!/usr/bin/env bash

case "${1:-}" in
    previous|play-pause|next|status-icon) action=$1 ;;
    *) exit 2 ;;
esac

playing_player=""
paused_player=""

while IFS= read -r player; do
    [[ -z "$player" ]] && continue
    status=$(playerctl --player="$player" status 2>/dev/null || true)

    if [[ "$status" == "Playing" ]]; then
        playing_player=$player
        break
    fi

    [[ "$status" == "Paused" && -z "$paused_player" ]] && paused_player=$player
done < <(playerctl --list-all 2>/dev/null)

target=${playing_player:-$paused_player}

if [[ "$action" == "status-icon" ]]; then
    if [[ -n "$playing_player" ]]; then
        printf '⏸\n'
    else
        printf '▶\n'
    fi
    exit 0
fi

[[ -n "$target" ]] && playerctl --player="$target" "$action"
