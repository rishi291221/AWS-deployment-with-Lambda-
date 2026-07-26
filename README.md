Automated S3 Bucket Cleanup (Objects Older Than 30 Days)
Objective: Automate deletion of stale objects in an S3 bucket.
Task: Delete files older than 30 days in a specific bucket.
Instructions:
1.	S3 Setup: Create a bucket and upload several files. (Since you can't easily create "old" objects, temporarily lower the age threshold to minutes for testing — then set it back to 30 days in the final code.)
2.	Lambda IAM Role: Inline policy with s3:ListBucket and s3:DeleteObject scoped to your bucket.
3.	Lambda Function (Python 3.12+, Boto3):
1.	List objects in the bucket (use the paginator — never assume one page of results).
2.	Compare each object's LastModified (timezone-aware) with the current UTC time.
3.	Delete objects older than 30 days.
4.	Print the names of deleted objects.
4.	Testing: Manually trigger and confirm only newer files remain.
5.	Discussion point (include in your documentation): In production, S3 Lifecycle Rules handle this natively with zero code. Explain in 2–3 lines when you'd use Lambda instead (e.g., conditional logic, naming patterns, cross-service actions).
