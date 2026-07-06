# Decision Log

## Activity ID Format

Decision: Use plain string IDs such as `2026-04-001` or `sample-2026-04-001`.

Do not use circled numbers as system identifiers.

Reason: Circled numbers are useful for newsletter display but poor as stable system primary keys.

## Validation Exit Codes

Decision:

- `0` = PASS
- `1` = validation failure
- `2` = tool execution error

Reason: Future runners must distinguish record validation failures from tool or runtime failures.

## Severity Defaults

Decision:

- Schema validation findings use severity `critical`.
- Business validation findings use severity defined by BR rule files.

Reason: Structural schema errors should stop downstream processing.
