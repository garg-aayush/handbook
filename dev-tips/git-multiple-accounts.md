# Using multiple GitHub accounts (per-repo identity)

Working with a personal and a work GitHub account on the same machine means three
*independent* identities, each configured in a different place. Getting all three
right is what makes a repo commit, push, and run `gh` as the correct account.

## Links
- [direnv](https://direnv.net/) (per-directory env loader; see [tools.md](tools.md))
- [git-scm: conditional includes (`includeIf`)](https://git-scm.com/docs/git-config#_conditional_includes)
- [gh environment variables (`GH_CONFIG_DIR`)](https://cli.github.com/manual/gh_help_environment)

## The three layers

| Layer | Controls | Where it is set |
|---|---|---|
| Commit identity | Name/email stamped on each commit | `git config user.*` (per repo) or `includeIf` (per directory tree) |
| Transport auth | `push` / `pull` / `fetch` | SSH host alias in `~/.ssh/config` + the remote URL |
| `gh` CLI | `gh pr`, `gh issue`, `gh api` | `gh` config dir, selected per repo with `direnv` + `GH_CONFIG_DIR` |

Getting only one or two right is the usual trap: commits look personal but push as
work, or `git` is personal but `gh pr create` opens the PR from the work account.

## 1. Commit identity

Per repo (run inside the repo):

```bash
git config user.name  "Aayush Garg"
git config user.email "garg-aayush@users.noreply.github.com"
```

To apply an identity automatically to every repo under a directory, add a conditional
include to `~/.gitconfig` (no per-repo command needed):

```gitconfig
[includeIf "gitdir:~/REPOS/personal/"]
    path = ~/.gitconfig-personal
```

```gitconfig
# ~/.gitconfig-personal
[user]
    name  = Aayush Garg
    email = garg-aayush@users.noreply.github.com
```

Using the GitHub `users.noreply` email keeps your real email private while still
attributing commits to the account.

## 2. Transport auth (SSH keys)

One SSH key per account, exposed as separate `Host` aliases in `~/.ssh/config`:

```sshconfig
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal

Host github-ac
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_ac
```

Point the repo's remote at the right alias (note `github-personal:` instead of
`github.com:`):

```bash
git remote set-url origin git@github-personal:garg-aayush/handbook.git
ssh -T git@github-personal          # -> "Hi garg-aayush! ..."
```

The alias, not the account, decides which key authenticates the push.

## 3. `gh` CLI identity (per repo, via direnv)

`gh` is a global tool with no native per-repo setting: it uses whichever account is
active. The fix is a separate `gh` config dir per account, selected automatically by
`direnv` when you enter the repo.

One-time setup:

```bash
# a) install direnv and hook it into the shell (Brewfile + zshrc already do this)
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# b) log the personal account into its own gh config dir (interactive, once)
GH_CONFIG_DIR=~/.config/gh-personal gh auth login
```

Per repo:

```bash
# .envrc in the repo root
echo 'export GH_CONFIG_DIR="$HOME/.config/gh-personal"' > .envrc
direnv allow .

# keep .envrc out of git without touching the tracked .gitignore
printf '%s\n' '.envrc' '.direnv/' >> .git/info/exclude
```

Now `cd` into the repo and `gh` is the personal account; leave and it reverts to the
default (work) account. Nothing about the work setup changes.

## Verify

```bash
cd ~/REPOS/handbook
git config user.email          # personal noreply email
git remote -v                  # origin uses github-personal:
gh auth status                 # active account = garg-aayush
```

## Gotchas

- **Already-open shells** do not have the new `direnv` hook. Run `exec zsh` or open a
  new terminal after editing `~/.zshrc`.
- **Fresh clone of a personal repo:** repeat the per-repo steps (remote alias, local
  `user.email` unless covered by `includeIf`, `.envrc` + `direnv allow`). The `gh`
  login in step 3b is machine-wide and only needed once.
- **`direnv` prints "is blocked":** you edited `.envrc`; re-run `direnv allow .` to
  trust the new contents.
