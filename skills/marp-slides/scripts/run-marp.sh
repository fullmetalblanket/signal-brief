#!/usr/bin/env bash
# Purpose: Render SignalBrief Marp decks with an installed CLI or approved on-demand npm execution.
# Public API: SIGNALBRIEF_APPROVE_PACKAGE_INSTALL=1 ./skills/marp-slides/scripts/run-marp.sh [marp arguments]
# Upstream deps: An installed marp command, or npm with access to @marp-team/marp-cli.
# Downstream consumers: The project-local marp-slides skill and agents following its workflow.
# Failure modes: Exits when neither Marp nor npm is available, or when package-install approval is absent.
# Performance: Uses an installed Marp command immediately; npm execution may download a package on first approved use.

set -euo pipefail

if command -v marp >/dev/null 2>&1; then
  exec marp "$@"
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "Marp is unavailable: install the public Marp CLI or provide npm for an approved on-demand run." >&2
  exit 1
fi

if [[ "${SIGNALBRIEF_APPROVE_PACKAGE_INSTALL:-}" != "1" ]]; then
  echo "Marp is not installed. Re-run with SIGNALBRIEF_APPROVE_PACKAGE_INSTALL=1 after package-install approval." >&2
  exit 1
fi

exec npm exec --yes --package @marp-team/marp-cli -- marp "$@"
