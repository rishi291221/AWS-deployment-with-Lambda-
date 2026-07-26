5.Restore an EC2 Instance from the Latest Snapshot
Objective: Automate disaster-recovery: rebuild an instance from its most recent EBS snapshot.
Instructions:
1.	Prerequisite: At least one snapshot of the source instance's root volume exists (Graded 2 pairs well here).
2.	Lambda IAM Role: ec2:DescribeSnapshots, ec2:RegisterImage (or ec2:CreateImage), ec2:RunInstances, ec2:DescribeImages, ec2:CreateTags.
3.	Lambda Function (Boto3):
1.	Find the most recent snapshot for the given volume/instance (sort describe_snapshots by StartTime).
2.	Register an AMI from the snapshot with register_image (specify root device mapping).
3.	Launch a new t3.micro instance from that AMI and tag it (e.g., RestoredFrom=<snapshot-id>).
4.	Print the new instance ID.
4.	Testing: Trigger manually; verify the new instance boots and contains the snapshot's data. Terminate test instances afterwards to avoid charges.
