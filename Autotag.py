import boto3
from datetime import datetime

ec2 = boto3.client("ec2")


def lambda_handler(event, context):

    # Extract instance ID from EventBridge event
    instance_id = event["detail"]["instance-id"]

    launch_date = datetime.utcnow().strftime("%Y-%m-%d")

    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {
                "Key": "LaunchDate",
                "Value": launch_date
            },
            {
                "Key": "Environment",
                "Value": "Development"
            }
        ]
    )

    print(f"Successfully tagged instance {instance_id}")

    return {
        "InstanceId": instance_id,
        "Status": "Tagged"
    }
