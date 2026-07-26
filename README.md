Auto-Tagging EC2 Instances on Launch
Objective: Automatically tag newly launched EC2 instances for resource tracking, ownership, and cost allocation.
Instructions:
1.	Lambda IAM Role: Inline policy with ec2:CreateTags and ec2:DescribeInstances.
2.	Lambda Function (Boto3):
1.	Extract the instance ID from the EventBridge event (detail.instance-id).
2.	Tag the instance with LaunchDate=<current date> and a custom tag (e.g., Owner or Environment).
3.	Print a confirmation message.
3.	EventBridge Rule: Create a rule matching event pattern — source aws.ec2, detail-type EC2 Instance State-change Notification, state running — with the Lambda as target.
4.	Testing: Launch a new instance; after a short delay, confirm the tags appear.
5.	Bonus: Extract the launching IAM user from CloudTrail events and add an Owner tag automatically — this is a popular interview scenario.
