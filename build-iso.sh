#!/usr/bin/env bash
set -euo pipefail

edition=${1-console}
case "$edition" in
    console) result=result ;;
    plasma) result=result-plasma ;;
    *) result= ;;
esac

if [[ $# -gt 1 || -z $result ]]; then
    printf 'Usage: %s [console|plasma]\n' "$0" >&2
    exit 2
fi

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
exec nix --extra-experimental-features 'nix-command flakes' build --no-update-lock-file \
    --out-link "$result" ".#iso-$edition"
