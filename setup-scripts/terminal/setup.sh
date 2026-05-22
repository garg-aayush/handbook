#!/usr/bin/env bash
#
# setup.sh — replicate the iTerm2 / zsh terminal environment on a new Mac.
# Idempotent: safe to re-run. Run from inside the terminal-migration folder:
#     bash setup.sh
#
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log()  { printf "\n\033[1;34m==> %s\033[0m\n" "$1"; }
warn() { printf "\033[1;33m[skip] %s\033[0m\n" "$1"; }

# 1. Homebrew -----------------------------------------------------------------
if ! command -v brew >/dev/null 2>&1; then
  log "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
# Load brew into this session (Apple Silicon path)
if [ -x /opt/homebrew/bin/brew ]; then eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then eval "$(/usr/local/bin/brew shellenv)"
fi

# 2. CLI tools from the Brewfile ---------------------------------------------
log "Installing CLI tools + casks from Brewfile (this is the long step)..."
brew bundle --file="$SCRIPT_DIR/Brewfile" || warn "Some Brewfile entries failed (often private taps) — continuing."

# 3. A Nerd Font for the Powerlevel10k icons ---------------------------------
log "Installing MesloLGS Nerd Font..."
brew install --cask font-meslo-lg-nerd-font || warn "font cask"

# 4. Oh My Zsh ----------------------------------------------------------------
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  log "Installing Oh My Zsh..."
  RUNZSH=no KEEP_ZSHRC=yes sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
else
  warn "Oh My Zsh already installed"
fi
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

# 5. Powerlevel10k theme ------------------------------------------------------
if [ ! -d "$ZSH_CUSTOM/themes/powerlevel10k" ]; then
  log "Installing Powerlevel10k..."
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$ZSH_CUSTOM/themes/powerlevel10k"
else
  warn "Powerlevel10k already installed"
fi

# 6. External zsh plugins -----------------------------------------------------
clone_plugin() {
  local name="$1" url="$2"
  if [ ! -d "$ZSH_CUSTOM/plugins/$name" ]; then
    log "Installing plugin: $name"
    git clone --depth=1 "$url" "$ZSH_CUSTOM/plugins/$name"
  else
    warn "plugin $name already installed"
  fi
}
clone_plugin zsh-autosuggestions     https://github.com/zsh-users/zsh-autosuggestions
clone_plugin zsh-syntax-highlighting https://github.com/zsh-users/zsh-syntax-highlighting

# 7. iTerm2 shell integration -------------------------------------------------
log "Installing iTerm2 shell integration..."
curl -fsSL https://iterm2.com/shell_integration/zsh -o "$HOME/.iterm2_shell_integration.zsh" || warn "iterm2 shell integration"

# 8. Dotfiles -----------------------------------------------------------------
log "Installing dotfiles (existing ones are backed up)..."
backup() { [ -f "$1" ] && cp "$1" "$1.backup-$(date +%Y%m%d%H%M%S)" && echo "  backed up $1"; }

backup "$HOME/.zshrc";  cp "$SCRIPT_DIR/zshrc" "$HOME/.zshrc"
backup "$HOME/.p10k.zsh"; cp "$SCRIPT_DIR/p10k.zsh" "$HOME/.p10k.zsh"

# 9. Default shell ------------------------------------------------------------
if [ "$(basename "${SHELL:-}")" != "zsh" ]; then
  log "Setting zsh as the default shell..."
  chsh -s "$(command -v zsh)" || warn "chsh — change the login shell manually if needed"
fi

cat <<'DONE'

==============================================================
 Done.
 Next steps you must do by hand:
   1. Import the iTerm2 appearance (theme/colors/font):
      iTerm2 -> Settings -> General -> Settings ->
      "Load preferences from a custom folder or URL" -> select THIS folder
      (it contains com.googlecode.iterm2.plist). See README.md, step 2.
   2. Set up the llm CLI (needed by the cmd/explain/pycode functions):
        llm keys set openai      # paste your OpenAI API key
   3. Restart iTerm2, or run:  exec zsh
   4. If the prompt looks off, run:  p10k configure
==============================================================
DONE
