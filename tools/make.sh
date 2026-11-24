#!/bin/sh
# Redraws ../assets/*.svg from the four repositories' git history.
# Expects clones of Research_paper, HJTK, Korean_voice and this repo side by side:
#   ./make.sh ../../research_paper ../../hjtk ../../korean_voice ..
set -e
cd "$(dirname "$0")"
mkdir -p logs fonts
for pair in "research_paper:$1" "hjtk:$2" "korean_voice:$3" "heok0308hth-glitch:$4"; do
  name=${pair%%:*}; dir=${pair#*:}
  TZ=Asia/Seoul git -C "$dir" log --reverse --shortstat --format='C|%ad|%s' \
    --date=format-local:'%Y-%m-%dT%H:%M' > "logs/log_$name.txt"
done
if [ ! -d fonts/pre ]; then
  (cd fonts && npm pack pretendard@1.3.9 @fontsource/jetbrains-mono@5.3.0 >/dev/null \
   && mkdir -p pre jbm && tar xzf pretendard-1.3.9.tgz -C pre && tar xzf fontsource-jetbrains-mono-5.3.0.tgz -C jbm)
fi
python3 build.py
