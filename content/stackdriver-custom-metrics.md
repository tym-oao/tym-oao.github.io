Title: Stackdriver custom metrics
Date: 2016-11-17 15:38:53
lat: 41.889197
long: -87.632898

The last item left to investigate/spike on for Postgres monitoring was setting up custom metrics via the Stackdriver API. This turns out to be fairly easy and quite flexible, and will be my recommendation for how we should proceed with filling in the [remaining monitoring items](http://devblog.ty-m.xyz/postgres-monitoring.html) that aren't addressed by Stackdriver and stackdriver-agent out of the box.

For python, connection to the API is managed via the usual `discovery` method in the official `google-api-python-client` library (and of course there are libraries for JS, Go, etc. as well).

Creation of a custom metric just requires provisioning a metric description and associating that to a metric type name. The basic structure of a metric is shown in the following python dictionary example:

```python
metrics_descriptor = {
    "type": custom_metric_type,
    "labels": [
        {
            "key": "environment",
            "valueType": "STRING",
            "description": "An arbitrary measurement"
        }
    ],
    "metricKind": metric_kind,
    "valueType": "INT64",
    "unit": "items",
    "description": "An arbitrary measurement.",
    "displayName": "Custom Metric"
}
```

The value in the `"type"` node is just an arbitrary value in the `custom.googleapis.com` namespace, for example 'custom.googleapis.com/postgres/connection_status'. The [`metricKind`](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.metricDescriptors#MetricKind) is generally one of 'GAUGE' or 'CUMULATIVE'. The `"labels"` provide a set of descriptive tags used to distinguish among specific instances of a metric type (e.g., a label might identify which Postgres instance a particular time series was coming from).

For writing data to a custom metric, we use the [`timeSeries.create`](https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/create) method. The structure looks complicated, but essentially we simply post a timestamp and data value to a given custom metric object for a resource. For example:

```python
timeseries_data = {
    "metric": {
        "type": 'custom.googleapis.com/trial_metric',
        "labels": {
            "pg_instance": "warehouse"
        }
    },
    "resource": {
        "type": 'gce_instance',
        "labels": {
            'instance_id':
            'gke-warehouse-provisioning-1-fde62020-node-l8ba',
            'zone': 'us-central1-f'
        }
    },
    "points": [
        {
            "interval": {
                "startTime": now,
                "endTime": now
            },
            "value": {
                "boolValue": True
            }
        }
    ]
}
```

Note it is also possible to create a new custom metric and start posting data to it in a single step.

The recommendation for resource is to use the physical layer on which the app being measured resides, although it is possible to set that to `gke_container`. [The docs have a full list of monitored resource types](https://cloud.google.com/monitoring/api/resources).

#### Conclusion
Using custom metrics for Postgres monitoring seems like the best bet. It may be possible to get something like [check_postgres](https://bucardo.org/wiki/Check_postgres) to produce output that can be read and posted to a custom metric. Or, since the number of checks to be added is relatively small compared to everything included in check_postgres, it might be easier to submit our own queries to Postgres using psycopg2 or whatever client, and then provision a TimeSeries object from that.

Although basic client connection to the Stackdriver API is provided by the standard `google-api-python-client` library, it will probably be worthwhile to provide a small helper module to generalize the task of creating and sending data to custom metrics from Postgres checks.
