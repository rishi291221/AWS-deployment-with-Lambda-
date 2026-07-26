import os
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
sns = boto3.client("sns")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):

    buckets = s3.list_buckets()["Buckets"]

    public_buckets = []

    for bucket in buckets:

        bucket_name = bucket["Name"]

        block_public = "Unknown"
        policy_public = False
        acl_public = False

        # Check Block Public Access
        try:
            response = s3.get_public_access_block(
                Bucket=bucket_name
            )

            config = response["PublicAccessBlockConfiguration"]

            block_public = all(config.values())

        except ClientError:
            # No Block Public Access configuration
            block_public = False

        # Check Bucket Policy Status
        try:
            response = s3.get_bucket_policy_status(
                Bucket=bucket_name
            )

            policy_public = response["PolicyStatus"]["IsPublic"]

        except ClientError:
            policy_public = False

        # Check Bucket ACL (legacy)
        try:
            acl = s3.get_bucket_acl(Bucket=bucket_name)

            for grant in acl["Grants"]:

                grantee = grant.get("Grantee", {})

                uri = grantee.get("URI", "")

                if "AllUsers" in uri or "AuthenticatedUsers" in uri:
                    acl_public = True

        except ClientError:
            pass

        if (not block_public) or policy_public or acl_public:

            public_buckets.append(bucket_name)

            print(f"Public Bucket Found: {bucket_name}")

    if public_buckets:

        message = "Public S3 Bucket(s) Detected\n\n"

        message += "\n".join(public_buckets)

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="S3 Public Access Alert",
            Message=message
        )

        print("SNS Alert Sent")

    else:

        print("No Public Buckets Found")

    return {
        "PublicBuckets": public_buckets
    }
