# Calendar Eligibility Subject Contract Draft

Status: inactive `calendar-eligibility-subject/0.3.0-draft`

The separately hashed subject contains exact owner-approved eligibility content: contract version, decision identity and supersession, run, activity, consumer, decision, required allowed fields, and prohibited uses. Calendar eligibility requires `activity_id`, `activity_title`, `dates`, and `time`.

It contains no authority reference or digest. Its generic envelope must use purpose and subject type `calendar-eligibility`, bind the exact subject ID/digest and run/activity/consumer scope, and obtain effect through ordinary anchored snapshot membership. Eligibility authority cannot authenticate selection, publication, run metadata, or revocation.
