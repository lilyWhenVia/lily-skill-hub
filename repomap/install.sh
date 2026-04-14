#!/bin/bash
mkdir -p ~/.claude/skills/repomap
curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/repomap/skill.md -o ~/.claude/skills/repomap/skill.md
curl -fsSL https://raw.githubusercontent.com/lilyWhenVia/lily-skill-hub/main/repomap/org.py -o ~/.claude/skills/repomap/org.py
echo "✓ /repomap installed"
