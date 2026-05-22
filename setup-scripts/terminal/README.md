# Setting up my terminal on a new Mac

Rought steps to set up terminal on a Mac. I have written these steps down so I can easily replicate them on a new Mac.

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
| `yazi.toml` | Yazi config → `~/.config/yazi/yazi.toml`. PDF preview via poppler; bat opener for text/JSON/MD/YAML. |

## Step 5b — Copy the yazi config

`yazi.toml` configures PDF preview (via `poppler`/`pdftoppm`) and a `bat` opener for text/JSON/Markdown/YAML files. Copy it after Step 2 (which installs both `yazi` and `poppler`):

```bash
mkdir -p ~/.config/yazi
cp yazi.toml ~/.config/yazi/yazi.toml
```

## Notes

- **No secrets in here.** API keys are intentionally left out. I add mine in
  `~/.secrets.zsh` and `source` it from `~/.zshrc` (or set them via the tool's
  own config, like `llm keys set` above).
- **Font:** the iTerm2 profile expects **MesloLGS NF**, which Step 2 installs. If
  glyphs ever look wrong, set the profile font to "MesloLGS NF" manually.
- **Tweaking later:** edit `~/.zshrc` for aliases/functions, run `p10k configure`
  to restyle the prompt, and re-run `brew bundle --file=Brewfile` any time to top
  up tools.
