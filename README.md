# monthly-agent

Tools and prompts for extracting activity information from elderly centre monthly programme documents.

The project focuses on turning monthly programme source documents into structured activity data that can be checked by QA workflows and later reused for monthly newsletter generation.

## Project Structure

- `data/input/` - source monthly programme documents or exported text.
- `data/output/` - extracted structured data and QA outputs.
- `docs/project-plan.md` - implementation plan and workflow notes.
- `prompts/extract-activity-info.md` - prompt for extracting activity data.
- `prompts/qa-check-monthly-info.md` - prompt for reviewing extracted monthly data.

## Workflow

1. Place source documents in `data/input/`.
2. Extract programme activity details into structured records.
3. Save extraction results in `data/output/`.
4. Run QA checks against the original source.
5. Use approved structured records for newsletter generation.
