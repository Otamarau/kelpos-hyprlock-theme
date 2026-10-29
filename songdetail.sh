#!/usr/bin/env bash

# Prefer a player that is actively playing. If every player is paused, show the
# first paused track so the lock screen still describes the current media.
metadata="$({
    playerctl --all-players metadata \
        --format '{{status}}:::{{artist}}:::{{title}}' 2>/dev/null || true
} | awk -F ':::' '
    $1 == "Playing" { print; found = 1; exit }
    $1 == "Paused" && paused == "" { paused = $0 }
    END { if (!found && paused != "") print paused }
')"

[[ -z "$metadata" ]] && exit 0

_status=${metadata%%:::*}
details=${metadata#*:::}
artist=${details%%:::*}
title=${details#*:::}
[[ -z "$title" ]] && exit 0

# Hyprlock renders label text as Pango markup, so escape metadata characters
# that would otherwise be interpreted as tags/entities.
escape_markup() {
    local value=$1
    value=${value//&/\&amp;}
    value=${value//</\&lt;}
    value=${value//>/\&gt;}
    printf '%s' "$value"
}

artist=$(escape_markup "$artist")
title=$(escape_markup "$title")

if [[ -n "$artist" ]]; then
    printf '%s — %s\n' "$artist" "$title"
else
    printf '%s\n' "$title"
fi
