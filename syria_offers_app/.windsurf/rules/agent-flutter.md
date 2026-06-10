# Agent Flutter Rules

Use local instructions in `.windsurf`.

## Rule Triggers
Apply the matching rule **before** making changes:
- `.windsurf/rules/shared/ui.md` — UI creation, widgets, tokens, localization, state coverage, PR checklist.
- `.windsurf/rules/shared/integration-api.md` — API integration: endpoints, models, repository, bloc wiring.
- `.windsurf/rules/shared/ui-refactor-convert.md` — Post-convert cleanup: rename, decompose, tokenize, localize.
- `.windsurf/rules/shared/ci-cd-pr.md` — Commit/push/PR gate after completing UI or API work.
- `.windsurf/rules/shared/unit-test.md` — Unit test standards.
- `.windsurf/rules/shared/widget-test.md` — Widget test standards.

## Skill Triggers
When a task matches a skill description, read `.windsurf/skills/<skill>/SKILL.md` before writing code.

## New Project Scaffolding
`bash .windsurf/scripts/bootstrap_flutter_template.sh`

## Quality Gate (Required Before Commit)
```bash
dart format lib test \
  && dart fix lib --apply --code=unused_import,duplicate_import,prefer_single_quotes \
  && dart fix test --apply --code=unused_import,duplicate_import,prefer_single_quotes
```

## Commit / Push / PR Gate
After completing any UI or API feature, ask the user in strict order:
1. `Do you want me to commit now? (yes/no)`
2. `Do you want me to push now? (yes/no)`
3. `Do you want me to create PR now? (yes/no)`
Execute only the steps confirmed with `yes`. Stop and report status on `no`.
