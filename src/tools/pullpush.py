import click
from ..utils.shell import run_shell_command

@click.command()
@click.option('--branch', default='main', help='The branch to pull from and push to.')
@click.option('--auto-commit', is_flag=True, help='Automatically commit uncommitted changes before pulling and pushing.')
@click.option('--commit-message', type=str, help='Custom commit message for auto-commit.')
@click.option('--stash', is_flag=True, help='Stash uncommitted changes before pulling and pop them after pushing.')
@click.option('--rebase', is_flag=True, help='Rebase local commits on top of the upstream branch after pulling.')
@click.option('--force-with-lease', is_flag=True, help='Use --force-with-lease when pushing. Use with caution!')
@click.option('--verbose', is_flag=True, help='Show detailed git status output.')
@click.option('--dry-run', is_flag=True, help='Show what commands would be executed without actually running them.')
@click.option('--interactive', is_flag=True, help='Pause for user intervention if merge conflicts occur after pulling.')
def pullpush(branch, auto_commit, commit_message, stash, rebase, force_with_lease, verbose, dry_run, interactive):
    """A command to pull and push changes to a git repository."""
    if auto_commit and stash:
        click.echo("Error: Cannot use --auto-commit and --stash together. Please choose one.")
        return
    if commit_message and not auto_commit:
        click.echo("Error: --commit-message can only be used with --auto-commit.")
        return
    if force_with_lease and dry_run:
        click.echo("Warning: --force-with-lease has no effect in --dry-run mode.")

    def execute_command(cmd, description):
        if dry_run:
            click.echo(f"[Dry Run] Would execute: {cmd} ({description})")
            return {"returncode": 0, "stdout": "", "stderr": ""}
        else:
            click.echo(f"Executing: {cmd} ({description})")
            result = run_shell_command(cmd)
            if verbose and result["stdout"]:
                click.echo(f"Stdout:\n{result["stdout"]}")
            if verbose and result["stderr"]:
                click.echo(f"Stderr:\n{result["stderr"]}")
            return result

    stashed = False
    if stash:
        click.echo("Checking for uncommitted changes to stash...")
        status_result = execute_command("git status --porcelain", "Check for uncommitted changes")
        if status_result["returncode"] != 0:
            click.echo("Error checking git status:")
            click.echo(status_result["stderr"])
            return

        if status_result["stdout"].strip():
            click.echo("Uncommitted changes detected. Stashing...")
            stash_result = execute_command("git stash push --include-untracked", "Stash uncommitted changes")
            if stash_result["returncode"] != 0:
                click.echo("Error stashing changes:")
                click.echo(stash_result["stderr"])
                return
            stashed = True
            click.echo("Changes stashed.")
        else:
            click.echo("No uncommitted changes to stash.")
    elif auto_commit:
        click.echo("Checking for uncommitted changes...")
        status_result = execute_command("git status --porcelain", "Check for uncommitted changes")
        if status_result["returncode"] != 0:
            click.echo("Error checking git status:")
            click.echo(status_result["stderr"])
            return

        if status_result["stdout"].strip():
            click.echo("Uncommitted changes detected.")
            if dry_run:
                click.echo("[Dry Run] Would auto-commit changes.")
            else:
                click.echo("Auto-committing...")
                add_result = execute_command("git add .", "Stage all changes")
                if add_result["returncode"] != 0:
                    click.echo("Error staging changes:")
                    click.echo(add_result["stderr"])
                    return

                commit_msg = commit_message if commit_message else "Auto-commit by bughunter-cli pullpush command"
                commit_result = execute_command(f"git commit -m \"{commit_msg}\"", "Commit staged changes")
                if commit_result["returncode"] != 0:
                    click.echo("Error auto-committing changes:")
                    click.echo(commit_result["stderr"])
                    return
                click.echo("Changes auto-committed.")
        else:
            click.echo("No uncommitted changes found.")

    if verbose:
        click.echo("\n--- Git Status Before Pull ---")
        execute_command("git status --short", "Current git status")
        click.echo("------------------------------")

    click.echo(f"Preparing to pull from {branch}...")
    pull_command = f"git pull origin {branch}"
    if rebase:
        pull_command = f"git pull --rebase origin {branch}"

    pull_result = execute_command(pull_command, f"Pull changes from origin/{branch}")
    if pull_result["returncode"] != 0:
        click.echo("Error pulling changes:")
        click.echo(pull_result["stderr"])
        if stashed:
            click.echo("Attempting to pop stashed changes...")
            execute_command("git stash pop", "Pop stashed changes")
        return

    # Check for merge conflicts after pull (or rebase conflicts)
    conflicts_detected = False
    if not dry_run:
        status_after_pull = run_shell_command("git status --porcelain")
        # Check for both merge conflicts (UU) and rebase conflicts (DD, AA, etc. - though UU is most common for merge)
        if "UU" in status_after_pull["stdout"] or "DD" in status_after_pull["stdout"] or "AA" in status_after_pull["stdout"]:
            conflicts_detected = True
            click.echo("\nConflicts detected after pull/rebase!")
            click.echo("Please resolve the conflicts manually, then add the resolved files and commit/continue rebase.")
            click.echo("Conflicting files:")
            for line in status_after_pull["stdout"].splitlines():
                if line.startswith("UU ") or line.startswith("DD ") or line.startswith("AA "):
                    click.echo(f"  - {line[3:]}")
            if interactive:
                click.echo("Exiting for manual conflict resolution. Re-run pullpush after resolving.")
                if stashed:
                    click.echo("Attempting to pop stashed changes...")
                    execute_command("git stash pop", "Pop stashed changes")
                return
            else:
                click.echo("Proceeding without interactive resolution. You may need to resolve conflicts manually.")

    if conflicts_detected and not interactive:
        click.echo("Skipping push due to unresolved conflicts.")
        if stashed:
            click.echo("Attempting to pop stashed changes...")
            execute_command("git stash pop", "Pop stashed changes")
        return

    click.echo("Preparing to push changes...")
    push_command = f"git push origin {branch}"
    if force_with_lease:
        push_command += " --force-with-lease"
        click.echo("Warning: Using --force-with-lease. This can overwrite remote history. Use with caution!")

    push_result = execute_command(push_command, f"Push changes to origin/{branch}")
    if push_result["returncode"] != 0:
        click.echo("Error pushing changes:")
        click.echo(push_result["stderr"])
        if stashed:
            click.echo("Attempting to pop stashed changes...")
            execute_command("git stash pop", "Pop stashed changes")
        return

    if verbose:
        click.echo("\n--- Git Status After Push ---")
        execute_command("git status --short", "Current git status")
        click.echo("-----------------------------")

    click.echo("Pull and push process completed (or simulated in dry-run mode).")
    if stashed:
        click.echo("Attempting to pop stashed changes...")
        execute_command("git stash pop", "Pop stashed changes")