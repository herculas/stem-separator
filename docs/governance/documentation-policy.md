# Documentation policy

| Material | Owning location |
| --- | --- |
| Project orientation and mandatory reading routes | Root `README.md` and `AGENTS.md` |
| Reading map | `docs/README.md` |
| Durable rules | `docs/governance/` |
| Current procedures, supported environments, and operating limits | `docs/operations/` |
| Superseded procedures, closed experiments, and dated validation records | `docs/history/` |
| Run logs, full outputs, and executed snapshots | The approved PolyU workspace or archive |

1. Read the [index](../README.md) and identify the guide that already owns the
   topic. Update that guide when the new material answers the same question.
   Give a new page a distinct purpose and link it from the nearest index.
2. Write in English. Use lowercase hyphen-separated names for Markdown files
   and documentation directories. Use `README.md` for indexes and `AGENTS.md`
   for agent instructions where needed. Prefer stable topic names and use dates
   in filenames for distinct historical records when they aid identification.
3. Put commands and current defaults in the operations guide. Use relative
   links to code, requirements, and other tracked documents. Keep credentials,
   personal paths, tunnel details, and unpublished run data out of the public repo.
4. When retiring a guide, move its still-valid instructions into the current
   owner. Preserve the historical outcome and limits in `docs/history/` with
   an explicit status and a link to the current guide. Preserve immutable
   evidence and original source revisions in Git or the approved archive.
5. Before staging, check incoming and outgoing links, heading anchors, path
   case, and reachability from the index. Check commands against the code and
   label proposed, historical, and verified behavior. Keep `AGENTS.md` focused
   on durable rules and mandatory reading routes.

The pre-commit hook checks documentation paths, common sensitive or bulk paths,
and staged object size. Review link targets, language, and factual claims when
reviewing the staged diff.
