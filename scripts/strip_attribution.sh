#!/usr/bin/env bash
# Rewrite Git history so an AI assistant identity is no longer a commit author/committer/co-author.
#   scripts/strip_attribution.sh repos.txt            # dry run: rewrite and verify locally, push nothing
#   scripts/strip_attribution.sh repos.txt --push     # also force-push changed refs (with leases)
# Per repository: fresh bare clone; backup bundle; delete merged fact-check/* branches; run
# git-filter-repo (https://github.com/newren/git-filter-repo) with strip_attribution_callback.py;
# verify (no assistant identity, no attribution lines on the owner's commits, every branch/tag tip
# has the same tree as before); then push each changed ref with --force-with-lease on the SHA just
# cloned, so nothing pushed meanwhile is overwritten. Other people's commits stay byte-identical.
# Needs: git, git-filter-repo (`uv tool install git-filter-repo`), push rights, and a git host that
# allows force-pushes. Afterwards re-clone or `git fetch && git reset --hard origin/<branch>` locally.
# A repository that fails verification or push is reported and skipped; the exit status is then 1.
# Works from Git Bash on Windows: python3's CRLF output is stripped, and git log is decoded as UTF-8.
set -euo pipefail
list=$1; push=${2:-}
here=$(cd "$(dirname "$0")" && pwd); W=${STRIP_WORKDIR:-$PWD/strip-work}; mkdir -p "$W"/{bundles,logs,maps,repos}
export STRIP_OLD_EMAIL=${STRIP_OLD_EMAIL:-noreply@anthropic.com}
export STRIP_NEW_NAME=${STRIP_NEW_NAME:?set STRIP_NEW_NAME, e.g. your GitHub username}
export STRIP_NEW_EMAIL=${STRIP_NEW_EMAIL:?set STRIP_NEW_EMAIL, e.g. 12345+you@users.noreply.github.com}
export STRIP_OWNER_REGEX=${STRIP_OWNER_REGEX:?set STRIP_OWNER_REGEX, a regex matching your author names/emails}
callback=$(cat "$here/strip_attribution_callback.py")
count() {  # "<assistant author/committer identities> <attribution lines on owner commits>"
  git -C "$1" log --all --format='%an %ae%x01%ae %ce%x02%B%x00' | python3 -c "
import sys,re,os
own=re.compile(os.environ['STRIP_OWNER_REGEX'],re.I); old=os.environ['STRIP_OLD_EMAIL']
line=re.compile(r'^\s*(co-authored-by:\s*claude.*|claude-session:.*|.*generated with \[?claude code.*|https://claude\.ai/code/session_\S*\s*)$',re.I)
ids=lines=0
for r in sys.stdin.buffer.read().decode('utf-8','surrogateescape').split('\x00'):  # not the locale codec
    if not r.strip(): continue
    who,rest=r.strip('\n').split('\x01',1); people,body=rest.split('\x02',1); ids+=people.lower().count(old)
    if own.search(who) or old in who.lower(): lines+=sum(1 for l in body.split('\n') if line.match(l))
print(ids, lines)" | tr -d '\r'; }  # Windows python3 prints "0 0\r\n"; "0\r" would fail the "00" checks
trees() { git -C "$1" for-each-ref --format='%(refname)' refs/heads refs/tags | while read r; do echo "$r $(git -C "$1" rev-parse "$r^{tree}")"; done; }
failed=()
while read slug; do
  [ -n "$slug" ] || continue; n=${slug#*/}; d=$W/repos/$n; url=https://github.com/$slug.git
  rm -rf "$d"; git clone -q --bare "$url" "$d"
  git -C "$d" for-each-ref --format='%(refname) %(objectname)' refs/heads refs/tags > "$W/logs/$n.leases"
  git -C "$d" bundle create -q "$W/bundles/$n.bundle" --all
  grep '^refs/heads/fact-check/' "$W/logs/$n.leases" | while read r s; do git -C "$d" update-ref -d "$r" "$s"; done || true
  trees "$d" > "$W/logs/$n.trees.before"; read ids0 lines0 < <(count "$d")
  if [ "$ids0$lines0" != 00 ]; then git -C "$d" filter-repo --force --quiet --commit-callback "$callback" >/dev/null
    cp "$d/filter-repo/commit-map" "$W/maps/$n.map"; fi
  read ids1 lines1 < <(count "$d"); trees "$d" > "$W/logs/$n.trees.after"
  same=$(cmp -s "$W/logs/$n.trees.before" "$W/logs/$n.trees.after" && echo yes || echo NO)
  specs=(); leases=()
  while read r old; do
    case $r in refs/heads/fact-check/*) leases+=("--force-with-lease=$r:$old"); specs+=(":$r"); continue;; esac
    new=$(git -C "$d" rev-parse "$r"); [ "$new" = "$old" ] || { leases+=("--force-with-lease=$r:$old"); specs+=("$new:$r"); }
  done < "$W/logs/$n.leases"
  echo "$n: identity $ids0->$ids1, attribution lines $lines0->$lines1, trees unchanged=$same, ref updates=${#specs[@]}"
  if [ "$ids1$lines1" != 00 ] || [ "$same" != yes ]; then echo "  verification failed; not pushing $n"; failed+=("$n"); continue; fi
  if [ "$push" = --push ] && [ ${#specs[@]} -gt 0 ]; then
    git -C "$d" push "${leases[@]}" "$url" "${specs[@]}" || { echo "  push failed for $n"; failed+=("$n"); }; fi
done < <(grep -v '^\s*#' "$list" | sed 's#https://github.com/##; s#\.git$##')  # no pipe: keeps $failed
echo "Backups: $W/bundles/*.bundle (restore: git clone <bundle>); old->new SHAs: $W/maps/*.map"
[ ${#failed[@]} -eq 0 ] || { echo "Failed (${#failed[@]}): ${failed[*]}"; exit 1; }
