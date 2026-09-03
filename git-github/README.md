# Git Homework Tasks

This README is a complete record of my Git practice. I performed the commands in a separate local repository called `git-practice-repo` inside this task folder. The commit IDs shown below are actual IDs created during this exercise.

## Task 1: `git commit -a -m` versus `git commit -m`

### Meaning of each command

| Command | What it does |
| --- | --- |
| `git commit -m "message"` | Commits only changes already placed in the staging area with `git add`. It does not automatically stage anything. |
| `git commit -a -m "message"` | Automatically stages modifications and deletions of **already tracked** files, then commits them. It does **not** add new untracked files; those still require `git add`. |

### Practice performed

First, I created and committed a tracked file:

```bash
git init -b main
git config user.name "Git Homework Student"
git config user.email "student@example.com"
git add notes.txt
git commit -m "Initial tracked notes"
```

Output:

```text
[main (root-commit) 46b0fa7] Initial tracked notes
 1 file changed, 1 insertion(+)
 create mode 100644 notes.txt
```

I then modified `notes.txt` but did not run `git add`.

```bash
git status --short
git commit -m "Attempt commit without staging"
```

Output:

```text
 M notes.txt
On branch main
Changes not staged for commit:
  modified:   notes.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

This proved that `git commit -m` did not commit my unstaged modification.

Next, I committed the same tracked-file modification using `-a`:

```bash
git commit -a -m "Save tracked notes with -a"
git log --oneline -2
```

Output:

```text
[main 27993e4] Save tracked notes with -a
 1 file changed, 1 insertion(+)
27993e4 Save tracked notes with -a
46b0fa7 Initial tracked notes
```

This proved that `git commit -a -m` automatically staged and committed the modified tracked file.

## Task 2: Git Cherry-Pick

### 1. Create commits on `main`

I created four commits on `main` (the task asked for 2–4):

```bash
git add main-checklist.txt
git commit -m "Add main branch checklist"
git add main-status.txt
git commit -m "Add main branch status file"
git log --oneline --decorate -4
```

Output:

```text
6727770 (HEAD -> main) Add main branch status file
fa06bf8 Add main branch checklist
27993e4 Save tracked notes with -a
46b0fa7 Initial tracked notes
```

### 2. Create a feature branch and commits

I created a branch named `feature-alerts` and made two commits in it:

```bash
git switch -c feature-alerts
git add feature-alert.txt
git commit -m "Add feature alert configuration"
git add feature-alert.txt
git commit -m "Enable feature alert notification"
git log --oneline --decorate -3
```

Output:

```text
9620cf9 (HEAD -> feature-alerts) Enable feature alert notification
a3e5eb6 Add feature alert configuration
6727770 (main) Add main branch status file
```

I selected commit `a3e5eb6` (`Add feature alert configuration`) to copy into `main`.

### 3. Cherry-pick the selected commit into `main`

```bash
git switch main
git cherry-pick a3e5eb6
```

Output:

```text
Switched to branch 'main'
[main 51ba5c7] Add feature alert configuration
 1 file changed, 1 insertion(+)
 create mode 100644 feature-alert.txt
```

The new commit ID is `51ba5c7`. Cherry-pick creates a new commit on the destination branch, so its ID differs from the original feature-branch commit even though it contains the same change.

### 4. Verify the result on `main`

```bash
git log --oneline --decorate -5
git show --stat --oneline HEAD
```

Output:

```text
51ba5c7 (HEAD -> main) Add feature alert configuration
6727770 Add main branch status file
fa06bf8 Add main branch checklist
27993e4 Save tracked notes with -a
46b0fa7 Initial tracked notes

51ba5c7 Add feature alert configuration
 feature-alert.txt | 1 +
 1 file changed, 1 insertion(+)
```

This verifies that the selected change is now available in `main`: `feature-alert.txt` was created by the cherry-picked commit.

## What I learned

- Use `git add` followed by `git commit -m` when I want explicit control over what is staged.
- Use `git commit -a -m` only for changes to files Git already tracks; new files must be added first with `git add`.
- `git log --oneline` is a quick way to identify commit IDs.
- `git cherry-pick COMMIT_ID` copies one specific commit from another branch to the current branch.

## Submission checklist

- [x] Practiced `git commit -m` and observed that unstaged changes were not committed.
- [x] Practiced `git commit -a -m` and observed that the tracked change was committed.
- [x] Created four commits in `main`.
- [x] Created two commits in `feature-alerts`.
- [x] Cherry-picked one selected feature commit into `main`.
- [x] Verified the cherry-picked change with `git log` and `git show`.
