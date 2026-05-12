#!/bin/bash
# Claude Code custom status line.
# Renders: [model] | dir | git-branch | $cost | Ctx:N%
#
# Install:
#   cp .claude/statusline.sh ~/.claude/statusline.sh
#   chmod +x ~/.claude/statusline.sh
#   brew install jq   # required
#
# Then in ~/.claude/settings.json:
#   "statusLine": {
#     "type": "command",
#     "command": "~/.claude/statusline.sh",
#     "padding": 0
#   }

input=$(cat)
 
MODEL=$(echo "$input" | jq -r '.model.display_name')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
PERCENT_USED=$(echo "$input" | jq -r '.context_window.used_percentage // 0')
 
# ANSI colors
ORANGE='\033[38;5;208m'
GREEN='\033[32m'
YELLOW='\033[33m'
RED='\033[31m'
CYAN='\033[36m'
RESET='\033[0m'
 
# Color context percentage based on usage
PERCENT_INT=$(printf '%.0f' "$PERCENT_USED")
if [ "$PERCENT_INT" -lt 50 ]; then
    CTX_COLOR=$GREEN
elif [ "$PERCENT_INT" -lt 80 ]; then
    CTX_COLOR=$YELLOW
else
    CTX_COLOR=$RED
fi
 
COST_FMT=$(printf '%.2f' "$COST")

BRANCH=$(git -C "$CURRENT_DIR" symbolic-ref --short HEAD 2>/dev/null || git -C "$CURRENT_DIR" rev-parse --short HEAD 2>/dev/null)
if [ -n "$BRANCH" ]; then
    BRANCH_SEG=" | ${YELLOW}${BRANCH}${RESET}"
else
    BRANCH_SEG=""
fi

echo -e "${ORANGE}[$MODEL]${RESET} | ${CURRENT_DIR##*/}${BRANCH_SEG} | ${CYAN}\$${COST_FMT}${RESET} | ${CTX_COLOR}Ctx:${PERCENT_INT}%${RESET}"
