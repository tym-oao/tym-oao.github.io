title: Distinct line items from DFP line item service
date: 2016-05-18
lat: 41.8888423
long: -87.63285241

Over time, the table `warehouse_hold.hold_dfp_line_item` has accumulated many rows for each line item. In most cases this is due to changes in the line item configuration or status; it is also due to overlapping attempts to bring the data up-to-date. In any case, Analytics is interested only in the most recent record for each item. As noted in [Trello](https://trello.com/c/ygfrMXJr/615-warehouse-etl-investigate-and-fix-line-item-discrepancies-between-dfp-and-hold-dfp-line-item-table), I created a new `hold_dfp_line_item_distinct` table, to include one record per line_item_id, based on maximum `last_modified_date_time` and `created_at` values.

Oddly (says I), while a CTE defined as

```
#!sql
select max(last_modified_date_time) as last_modified_date_time
     , max(created_at) as created_at
     , line_item_id
  from hold_dfp_line_item
 group by 3
```
has the expected number of rows, joining that on all three columns back to the main table resulted in a small number (39 out of about a million) of duplicate rows.

I have been able to resolve the matter by using `select distinct`  in the main query, but I don't understand why it should be necessary.

Also, as we update with new pulls from the line item service, we'll begin to have multiple rows per line item again, and if this simplified table is desirable in Hold, we'll have to keep refreshing it. Therefore, we will eventually find out whether the duplication of the same line item at the same created_at timestamp was a one-time glitch, or something ongoing. In the former case, we should remove the `distinct` from the query, for performance reasons. This note is here as a reminder
