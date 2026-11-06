# git-filter-repo --commit-callback body: map an assistant identity to the owner and strip assistant
# attribution lines, only on the owner's own commits (other people's commits stay byte-identical).
import os, re
OLD_EMAIL = os.environ["STRIP_OLD_EMAIL"].encode()            # e.g. noreply@anthropic.com
NEW_NAME = os.environ["STRIP_NEW_NAME"].encode()              # e.g. BurnyCoder
NEW_EMAIL = os.environ["STRIP_NEW_EMAIL"].encode()            # owner's GitHub noreply address
OWNER = re.compile(os.environ["STRIP_OWNER_REGEX"].encode(), re.I)   # matches owner name/email
LINE = re.compile(rb"^\s*(co-authored-by:\s*claude.*|claude-session:.*|.*generated with \[?claude code.*"
                  rb"|https://claude\.ai/code/session_\S*\s*)$", re.I)
own = commit.author_email == OLD_EMAIL or OWNER.search(commit.author_name + b" " + commit.author_email)
if commit.author_email == OLD_EMAIL:
    commit.author_name, commit.author_email = NEW_NAME, NEW_EMAIL
if commit.committer_email == OLD_EMAIL:
    commit.committer_name, commit.committer_email = NEW_NAME, NEW_EMAIL
if own:
    lines = commit.message.split(b"\n")
    kept = [l for l in lines if not LINE.match(l)]
    if kept != lines:
        commit.message = b"\n".join(kept).rstrip(b"\n") + b"\n"
