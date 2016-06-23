title: Slowly-changing dimension handling for dim_line_item
date: 2016-05-09
lat: 41.8888423
long: -87.6328524

- Hold table load is somewhat incremental already: all modified items get added on to the hold table (not really distinguished from prior versions, but we can use `last_modified_date_time` for that)
- So, pull for `dim_line_item` update begins by taking all records with most recent `created_at` timestamps from `hold_dfp_line_item`.
- These can be inserted directly to `dim_line_item`, with `current_date` as `effective_dt` and `created_at`
- Then find `line_item_code` values that match newly-inserted rows, with prior `created_at` and NULL `effective_end_dt`
- update `effective_end_dt` of those rows with current_date
- **TL;DR**: treat line_item_code as the fixed SCD key; treat change in any other column as requiring a new record.
