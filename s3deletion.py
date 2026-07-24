# Replace with your bucket name
BUCKET_NAME = " mys3demo-123456"

# -----------------------------
# Testing
# Change to:
# AGE_THRESHOLD = timedelta(minutes=5)
#
# Production
# AGE_THRESHOLD = timedelta(days=30)
# -----------------------------
AGE_THRESHOLD = timedelta(days=30)

s3 = boto3.client("s3")


def lambda_handler(event, context):

    now = datetime.now(timezone.utc)

    paginator = s3.get_paginator("list_objects_v2")

    deleted = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):

        if "Contents" not in page:
            continue

        for obj in page["Contents"]:

            last_modified = obj["LastModified"]

            if now - last_modified > AGE_THRESHOLD:

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=obj["Key"]
                )

                print(f"Deleted: {obj['Key']}")

                deleted.append(obj["Key"])

    return {
        "statusCode": 200,
        "deleted_objects": deleted
    }
