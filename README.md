2.Automated EBS Snapshot Creation and Cleanup
Objective: Automate EBS volume backups and delete snapshots older than a retention period.
Instructions:
1.	EBS Setup: Identify or create an EBS volume; note the volume ID.
2.	Lambda IAM Role: Inline policy with ec2:CreateSnapshot, ec2:DescribeSnapshots, ec2:DeleteSnapshot, ec2:CreateTags.
3.	Lambda Function (Boto3):
1.	Create a snapshot of the specified volume and tag it (e.g., CreatedBy=Lambda-Backup).
2.	List snapshots with that tag (owned by your account) and delete those older than 30 days.
3.	Print IDs of created and deleted snapshots.
4.	EventBridge: Schedule the function weekly.
5.	Testing: Trigger manually; confirm snapshot creation and cleanup in the EC2 console.
6.	Discussion point: AWS Data Lifecycle Manager (DLM) does this natively. Note in your documentation when Lambda is still the better choice (custom retention logic, cross-account copies, notifications).

