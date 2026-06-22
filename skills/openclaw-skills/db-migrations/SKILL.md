---
name: db-migrations
description: >
  Execute database schema migrations for Next.js/Prisma projects.
  Use when the user mentions: database migration, prisma migrate, sync schema,
  apply migration, db deploy, schema push, or reset database.
metadata: { "openclaw": { "requires": { "bins": ["node", "npx"] }, "env": ["DATABASE_URL"] } }
---

# DB Migrations (Prisma)

## When to use
- User says "run migration" / "apply migration" / "prisma migrate deploy"
- "sync database schema" / "db deploy" / "update schema" / "reset db"

## How to invoke

Use the `exec` tool to run the skill entrypoint:

```bash
bash "{baseDir}/run.sh" "<project_dir>"
```

Where `<project_dir>` is the absolute path to the Next.js project root
(containing `package.json` and `prisma/schema.prisma`).

The script:
1. Validates inputs
2. Confirms `DATABASE_URL` is set
3. Runs `npx prisma migrate deploy`
4. Appends results to `D:/bobo/skill-test.log`

## Parameters (pass as shell arg)
- `$1` = project directory (absolute path)

## Exit codes
- `0` = migration applied / graceful skip
- non-zero = error (see log)

## Notes
- This skill is **read-write to the database** — confirm environment before running.
