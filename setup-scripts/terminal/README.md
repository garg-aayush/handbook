# Setting up my terminal on a new Mac

This is how I set up my terminal whenever I get a new Mac: **iTerm2** with the
**Powerlevel10k** prompt, fuzzy search (`fzf`), fish-style autosuggestions,
syntax highlighting, and the CLI tools I use day to day. Everything I need lives
in this folder, so I just work through the steps below in order. You can follow
the exact same steps to reproduce the setup.

When I'm done I have:

- iTerm2 with my theme, colors, and the **MesloLGS NF** font
- a Powerlevel10k prompt
- search & completion: `Ctrl+R` history / `Ctrl+T` files / `Alt+C` cd (fzf),
  grey inline autosuggestions (accept with `→`), and command syntax highlighting
- CLI tools like `bat`, `eza`, `fd`, `ripgrep`, `zoxide`, `glow`, `jq`, `yazi`,
  `btop`, `uv`, `llm` — all listed (and commented) in the `Brewfile`

---

## Step 0 — Install iTerm2 first

These steps configure iTerm2 but don't install it, so I install it before
anything else:

- Download: **https://iterm2.com/downloads.html**  (homepage: https://iterm2.com)
- Or, if Homebrew is already there: `brew install --cask iterm2`

Open iTerm2 once so it exists, then do everything below **inside iTerm2**.

## Step 1 — Get these files onto the machine

Clone the handbook and move into this folder:

```bash
git clone https://github.com/garg-aayush/handbook.git
cd handbook/setup-scripts/terminal
```

## Step 2 — Run the setup script

```bash
bash setup.sh
```

It's safe to re-run, and it does the heavy lifting:

- installs Homebrew (if missing) and everything in `Brewfile`
- installs the MesloLGS Nerd Font
- installs Oh My Zsh, Powerlevel10k, and the `zsh-autosuggestions` /
  `zsh-syntax-highlighting` plugins
- installs iTerm2 shell integration
- copies `zshrc` → `~/.zshrc` and `p10k.zsh` → `~/.p10k.zsh`
  (any existing files are backed up first)
- sets zsh as the default shell

## Step 3 — Import the iTerm2 look (theme, colors, font)

The settings live in `com.googlecode.iterm2.plist` in this folder. I use option A;
option B is a one-time copy.

**A. Point iTerm2 at this folder (what I do — stays in sync):**
iTerm2 → Settings (`⌘,`) → **General → Settings** →
check **"Load preferences from a custom folder or URL"** →
select **this `terminal/` folder** → quit and reopen iTerm2.

**B. One-time copy:**
```bash
osascript -e 'quit app "iTerm"'
cp com.googlecode.iterm2.plist ~/Library/Preferences/
killall cfprefsd
```
Then reopen iTerm2.

## Step 4 — Set up the `llm` CLI (Simon Willison's tool)

`llm` is installed by Step 2 and powers my `cmd`, `explain`, `image_qa`, and
`pycode` shell functions (defined in `~/.zshrc`). It needs an **OpenAI API key**.

Set the key once (it's stored in `llm`'s own config, not in any dotfile):

```bash
llm keys set openai
# paste your OpenAI API key when prompted
```

Get a key at https://platform.openai.com/api-keys · docs: https://llm.datasette.io

Check it works:

```bash
llm "say hello in one word"
```

> The helper functions reference specific model names (e.g. `CMD_LLM`) near the
> bottom of `~/.zshrc` — change them to models you actually have access to.

## Step 5 — Finish

Restart iTerm2 (or run `exec zsh`). If the prompt looks off, run `p10k configure`.

---

## What's in this folder

| File | What it is |
|------|------------|
| `setup.sh` | The installer from Step 2. Idempotent. |
| `Brewfile` | Homebrew taps/formulae/casks, each line commented. |
| `zshrc` | Becomes `~/.zshrc` (aliases, plugins, helper functions). |
| `p10k.zsh` | Powerlevel10k prompt config → `~/.p10k.zsh`. |
| `com.googlecode.iterm2.plist` | iTerm2 preferences (theme, colors, font, profile). |

## Notes

- **No secrets in here.** API keys are intentionally left out. I add mine in
  `~/.secrets.zsh` and `source` it from `~/.zshrc` (or set them via the tool's
  own config, like `llm keys set` above).
- **Font:** the iTerm2 profile expects **MesloLGS NF**, which Step 2 installs. If
  glyphs ever look wrong, set the profile font to "MesloLGS NF" manually.
- **Tweaking later:** edit `~/.zshrc` for aliases/functions, run `p10k configure`
  to restyle the prompt, and re-run `brew bundle --file=Brewfile` any time to top
  up tools.
