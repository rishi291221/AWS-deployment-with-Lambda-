import boto3
from datetime import datetime, timedelta, timezone

ec2 = boto3.client("ec2")

# Replace with your EBS Volume ID
VOLUME_ID = "vol-0123456789abcdef0"

# Testing:
# RETENTION = timedelta(minutes=5)

# Production:
RETENTION = timedelta(days=30)


def lambda_handler(event, context):

    now = datetime.now(timezone.utc)

    # Create Snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated Lambda Backup"
    )

    snapshot_id = snapshot["SnapshotId"]

    # Tag Snapshot
    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {
                "Key": "CreatedBy",
                "Value": "Lambda-Backup"
            }
        ]
    )

    print(f"Created Snapshot: {snapshot_id}")

    deleted = []

    paginator = ec2.get_paginator("describe_snapshots")

    pages = paginator.paginate(
        OwnerIds=["self"],
        Filters=[
            {
                "Name": "tag:CreatedBy",
                "Values": ["Lambda-Backup"]
            }
        ]
    )

    for page in pages:

        for snap in page["Snapshots"]:

            start_time = snap["StartTime"]

            if now - start_time > RETENTION:

                ec2.delete_snapshot(
                    SnapshotId=snap["SnapshotId"]
                )

                print(f"Deleted Snapshot: {snap['SnapshotId']}")

                deleted.append(snap["SnapshotId"])

    return {
        "CreatedSnapshot": snapshot_id,
        "DeletedSnapshots": deleted
    }
