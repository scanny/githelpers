_githelpers_ is a collection of Git helper scripts that ease _continuous spiking_ and
other grooming of a Git working branch.


Installation
============

```zsh
pip install 'git+https://github.com/scanny/githelpers#egg=githelpers'
```

To **uninstall**:

```zsh
pip uninstall githelpers
```


Usage
=====

Installing `githelpers` adds 5 new command-line commands:

* `git-lawg` -- Used as `$ git lawg`, but almost always used via one of several aliases
  described below.
* `fix` -- Add a `fixit` (cursor) branch and position it at the commit-ish provided as
  an argument. Moves the current `fixit` branch if it exists (unless it is dirty).
* `next` -- Move the `fixit` branch to the next commit.
* `prev` -- Move the `fixit` branch to the previous commit.
* `drop` -- Remove the (presumably spurious) commit provided as the argument.


Recommended aliases
===================

On `zsh`, `~/.zshrc` is generally a good place for these. You can add additional
parameters to each of these to extend to a particular purpose, like:

```zsh
$ gl my-branch-172404175
```


**Log-related:**

```zsh
# --- g-it h-ead - HEAD commit, on one line ---
alias gh='git lawg -1'

# --- g-it l-og - all commits, one per line, starting with HEAD, using a pager. Note
# --- this is a *function* rather than an alias, so it can take one or more branch
# --- names as arguments.
gl() { git lawg $@ | less -EFXRS }

# --- g-it l-og a-ll (branches) - all commit in all branches, using a pager. ---
alias gla='gl --all'

# --- g-it l-og r-ecent - 42 is adjustable for your preference, possibly determined
# --- by your typical terminal window height. Not paged.
alias glr='git lawg -42'

# --- g-it l-og r-ecent a-ll - most-recent N commits including all branches. This
# --- command is probably the most commonly used, but can be noisy when the most
# --- recent commits are not yours.
alias glra='git lawg -42 --all'

# --- g-it l-og r-ecent f-ixit - most-recent N commits on fixit branch. Not often
# --- used but occasionally handy.
alias glrf='glr fixit'

# --- g-it l-og r-ecent s-pike - most-recent N commits on spike branch. Frequently
# --- used when glra is noisy, but will not include fixit branch if it is not on
# --- spike branch.
alias glrs='glr spike'

# --- g-it l-og r-ecent s-pike f-ixit - most-recent N commits on both spike and
# --- fixit branch. This shows all interesting commits when fixit has branched and
# --- spike has not yet been rebased onto it.
alias glrsf='glr spike fixit'
```


**Other `githelpers` aliases**:

```zsh
alias n=next
alias p=prev


**Other Git aliases:**

```zsh
alias ga='git add'
alias gaa='git add --all'
alias gai='git add --interactive'

alias gb='git --no-pager branch'

alias gc='git commit -v'
alias gca='git commit -v --amend'
alias gcar='git commit --amend --reuse-message=HEAD'

alias gcl='git config --list'

# --- show the current conflicted commit when rebase stops for a merge conflict ---
alias gcm='cat .git/rebase-merge/message'

alias gco='git checkout'
alias gcof='git checkout fixit'
alias gcom='git checkout master'
alias gcos='git checkout spike'

alias gcp='git cherry-pick'
alias gcpc='git cherry-pick --continue'
alias gcpnc='git cherry-pick --no-commit'

alias gd='git diff'
alias gdc='git diff --cached'

# --- git HEAD, on one line ---
alias gh='git lawg -1'

alias gm='git merge'

# --- g-it p-atch - show patch/diff for HEAD ---
alias gp='git log -p -1 --oneline HEAD'

alias grb='git rebase'
alias grba='git rebase --abort'
alias grbc='git rebase --continue'
alias grbi='git rebase -i'
alias grbo='git rebase --onto'
alias grbs='git rebase --skip'

alias grsh='git reset --hard'
alias grsH='git reset HEAD'

alias gs='git status'
```
