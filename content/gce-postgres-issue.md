Title: Corrupt database disk issue at GCE
Date: 2016-06-29 22:54:20 +0000
lat: 41.8828766952614
long: -87.64016439234

Posting this here mainly in case this issue happens to come up again. I've noticed several cases in recent cloud console Notification Activity in which repeated disk-attachment errors were reported. In those cases I didn't notice any database service outages, but this still seems like something that could end up not being an isolated incident.

### Problem

- Between 22:10 and 22:20 on 2016-06-29, the Google cloud console Activity record shows that the persistent disks mounted to nodes in the `warehouse-provisioning-1` k8s cluster detached themselves from the instances they had been attached to.
- I say "detached themselves" because neither myself nor anyone at OAO executed any k8s commands to explicitly detach them. The root cause for the detachment is uncertain.
- The timing of [this SSD latency incident incident](https://status.cloud.google.com/incident/compute/16011) from the GCE [status page](https://status.cloud.google.com) seems to coincide with when these detachments happened. I imagine that disks might have had to be detached and reattached as part of whatever Google engineers did to resolve the issue, but that's a guess on my part.
- In any case, while the disks were also automatically reattached, the abrupt disconnection left them in an inconsistent state, so that Postgres instances which use these disk mounts for storage were unable to start due to I/O errors.
- Result: `warehouse-postgres` and `mart-postgres` instances were down since roughly 22:19.

### Resolution

Basically, to get things working again, I had to `fsck` the affected disks, then detach them from the instances they were attached to with a `gcloud` command. So, for example, in the case of the disk `mart-data-disk` attached to `warehouse-provisioning-1-fde62020-node-8n9r` I had to:

```
#!bash
ssh warehouse-provisioning-1-fde62020-node-8n9r \
sudo fsck.ext4 -v -y /dev/disk/by-id/google
gcloud compute instances detach-disk \
gke-warehouse-provisioning-1-fde62020-node-8n9r --disk mart-data-disk
```


Then restart the `mart-postgres` as usual with `kubectl create -f mart-postgres.yaml`.
