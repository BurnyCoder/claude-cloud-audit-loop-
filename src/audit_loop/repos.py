"""Repository list parsing and shallow clones into the work directory."""

import re
import subprocess
from pathlib import Path

_SLUG = re.compile(r"(?:https?://github\.com/|git@github\.com:)?([\w.-]+/[\w.-]+?)(?:\.git)?/?$")


def parse_repos(text: str) -> list[str]:
    """``owner/name`` per non-empty line; accepts GitHub URLs; ``#`` starts a comment; keeps order, drops repeats."""
    slugs: list[str] = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        match = _SLUG.fullmatch(line)
        if not match:
            raise ValueError(f"not a GitHub repository: {line!r}")
        if match.group(1) not in slugs:
            slugs.append(match.group(1))
    return slugs


def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def clone(slug: str, workdir: Path, branch: str) -> Path:
    """Shallow-clone (or refresh) ``slug`` and check out a fresh ``branch`` from the default branch.

    Refreshing discards local state in the clone, so every audit starts from the remote's
    current default branch. ``git fetch --unshallow`` gives the agent full history if needed.
    """
    path = workdir / slug.split("/")[1]
    if not (path / ".git").exists():
        workdir.mkdir(parents=True, exist_ok=True)
        git("clone", "--depth", "1", f"https://github.com/{slug}.git", str(path))
    default = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", cwd=path).removeprefix("origin/")
    git("fetch", "--depth", "1", "origin", default, cwd=path)
    git("checkout", "-f", "-B", branch, f"origin/{default}", cwd=path)
    git("clean", "-fdx", "-q", cwd=path)
    return path
