import os
import time
import boto3

ec2 = boto3.client("ec2")

VOLUME_ID = os.environ["VOLUME_ID"]
SUBNET_ID = os.environ["SUBNET_ID"]
SECURITY_GROUP_ID = os.environ["SECURITY_GROUP_ID"]
KEY_NAME = os.environ.get("KEY_NAME")

def lambda_handler(event, context):

    # Find latest snapshot
    response = ec2.describe_snapshots(
        Filters=[
            {
                "Name": "volume-id",
                "Values": [VOLUME_ID]
            }
        ],
        OwnerIds=["self"]
    )

    snapshots = sorted(
        response["Snapshots"],
        key=lambda x: x["StartTime"],
        reverse=True
    )

    if not snapshots:
        raise Exception("No snapshots found.")

    latest_snapshot = snapshots[0]

    snapshot_id = latest_snapshot["SnapshotId"]

    print(f"Latest Snapshot: {snapshot_id}")

    ami_name = f"restore-{snapshot_id}"

    # Register AMI
    image = ec2.register_image(
        Name=ami_name,
        RootDeviceName="/dev/xvda",
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/xvda",
                "Ebs": {
                    "SnapshotId": snapshot_id,
                    "DeleteOnTermination": True,
                    "VolumeType": "gp3"
                }
            }
        ],
        VirtualizationType="hvm",
        Architecture="x86_64"
    )

    image_id = image["ImageId"]

    print(f"AMI Created: {image_id}")

    # Wait until the AMI becomes available
    waiter = ec2.get_waiter("image_available")
    waiter.wait(ImageIds=[image_id])

    # Launch EC2 instance
    run_args = {
        "ImageId": image_id,
        "InstanceType": "t3.micro",
        "MinCount": 1,
        "MaxCount": 1,
        "SubnetId": SUBNET_ID,
        "SecurityGroupIds": [SECURITY_GROUP_ID],
        "TagSpecifications": [
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "RestoredFrom",
                        "Value": snapshot_id
                    }
                ]
            }
        ]
    }

    if KEY_NAME:
        run_args["KeyName"] = KEY_NAME

    response = ec2.run_instances(**run_args)

    instance_id = response["Instances"][0]["InstanceId"]

    print(f"Restored Instance: {instance_id}")

    return {
        "Snapshot": snapshot_id,
        "AMI": image_id,
        "Instance": instance_id
    }
