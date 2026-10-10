#!/usr/bin/env bash
# Construit le site et le met en ligne : remplace le contenu de la branche gh-pages
# (servie par GitHub Pages sur www.contactapaisement-mental.fr) par site/_build/.
set -euo pipefail
DEPOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$DEPOT/site/outils/construire.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$TMP"
git init -q
git remote add origin "$(git -C "$DEPOT" remote get-url origin)"
if git fetch -q origin gh-pages 2>/dev/null; then
  git checkout -q -b gh-pages FETCH_HEAD
else
  git checkout -q --orphan gh-pages
fi
git rm -rq --ignore-unmatch . >/dev/null
cp -r "$DEPOT/site/_build/." .
git add -A
if git diff --cached --quiet; then
  echo "Aucun changement à publier."
  exit 0
fi
MESSAGE="Site : publication du $(date -u '+%Y-%m-%d %H:%M') UTC"
if [ -n "${PIED_COMMIT:-}" ]; then MESSAGE="$MESSAGE

$PIED_COMMIT"; fi
if git config user.email >/dev/null; then
  git commit -q -m "$MESSAGE"
else
  git -c user.name="robot-pins" -c user.email="robot-pins@users.noreply.github.com" commit -q -m "$MESSAGE"
fi
git push -q origin gh-pages
echo "Publié sur la branche gh-pages."
# Le registre des dates du plan du site change quand une page change : il doit suivre le dépôt (main).
if [ -n "$(git -C "$DEPOT" status --porcelain -- site/outils/dates-contenu.json)" ]; then
  echo "À committer sur main : site/outils/dates-contenu.json (dates de mise à jour du plan du site)."
fi
