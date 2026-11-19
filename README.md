# Cedar calendar audit — Hermes skill tap

A self-contained custom Hermes skill that identifies calendar conflicts and available focus blocks from local exported JSON. Uses Python's standard library; no Google account, MCP server, credentials, or network access is needed by the helper.

The repository follows Hermes' default tap layout: `skills/cedar-calendar-audit/SKILL.md`, with referenced Python scripts and a fictional example. Add this repository with `hermes skills tap add anchalaa/cedar-hermes-skills`, search for `cedar-calendar-audit`, and install the repository/path identifier shown by Hermes. Use the source commit recorded with your installation evidence to reproduce the published version.

After installation, ask Hermes: “Use cedar-calendar-audit on its fictional Bluebird example for November 19, 2026, in America/Los_Angeles. Find conflicts and 60-minute focus blocks. Run the bundled helper and report the observed result.”

The skill does not infer that a partial export is a complete calendar, expand recurrence rules, change events, send messages, or read Google credentials. All-day events use exclusive end dates; cancelled and transparent events do not block time. The working day is 09:00–17:00. Input validation rejects reversed times and unexpanded recurrence rules.

Created for the CSCI 599 personal-assistant assignment with Codex assistance. The interval logic was adapted from the assignment project's calendar adapter. The student must review and understand the implementation. Synthetic data only is included.

Hermes documentation: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
