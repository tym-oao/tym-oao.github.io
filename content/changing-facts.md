title: Handling fact updates
date: 2016-05-11 07:24:35
lat: 41.8888423 
long: -87.6328524

- [Accumulating snapshot](http://decisionworks.com/2010/12/design-tip-130-accumulating-snapshots-for-complex-workflows/) fact table pattern sounded attractive, but we cannot apply it to our case. It is a way of handling late-arriving facts, but supposes access to the transactional workflow milestone data.
- In our case, DFP is already returning us pre-aggregated snapshot data; they restate the snapshot data over time as more atomic data accumulates on their end.
- For this reason, the best approach will be to reload over a reasonable window to keep our fact table records current with the latest stated values from DFP
- Exact number of days in the window TBD based on analysis of recent re-pulls of data we have already loaded.
- Best guess as of now: 14-day reload window (requires further investigation to rule out first-of-month being exceptional)
