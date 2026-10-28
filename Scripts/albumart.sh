#!/usr/bin/env bash

cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/hyprlock"
art_file="$cache_dir/album-art"
url_file="$cache_dir/album-art.url"

metadata="$({
    playerctl --all-players metadata \
        --format '{{status}}:::{{mpris:artUrl}}' 2>/dev/null || true
} | awk -F ':::' '
    $1 == "Playing" && $2 != "" { print; found = 1; exit }
    $1 == "Paused" && $2 != "" && paused == "" { paused = $0 }
    END { if (!found && paused != "") print paused }
')"

art_url=${metadata#*:::}
[[ -z "$metadata" || -z "$art_url" ]] && exit 0

if [[ "$art_url" == file://* ]]; then
    local_art=${art_url#file://}
    [[ -r "$local_art" ]] && printf '%s\n' "$local_art"
    exit 0
fi

[[ "$art_url" != http://* && "$art_url" != https://* ]] && exit 0

mkdir -p "$cache_dir"

cached_url=""
[[ -r "$url_file" ]] && IFS= read -r cached_url < "$url_file"

if [[ "$art_url" != "$cached_url" || ! -s "$art_file" ]]; then
    temporary="$art_file.$$"
    if curl --fail --location --silent --show-error \
        --connect-timeout 2 --max-time 5 \
        --output "$temporary" "$art_url" && [[ -s "$temporary" ]]; then
        mv -f "$temporary" "$art_file"
        printf '%s\n' "$art_url" > "$url_file"
    else
        rm -f "$temporary"
    fi
fi

[[ -s "$art_file" ]] && printf '%s\n' "$art_file"
