4.Daily AWS Cost Alert Using Cost Explorer API and SNS
Objective: Build an automated alert when AWS spend exceeds a threshold.
Note: The old CloudWatch "Billing" metric is legacy — it only exists in us-east-1 and must be manually enabled. The modern, interview-relevant approach uses the Cost Explorer API (ce:GetCostAndUsage).
Instructions:
1.	SNS Setup: Create a topic and subscribe your email (confirm the subscription email).
2.	Lambda IAM Role: Inline policy with ce:GetCostAndUsage and sns:Publish (scoped to your topic).
3.	Lambda Function (Boto3):
1.	Initialize ce and sns clients.
2.	Query month-to-date UnblendedCost with get_cost_and_usage.
3.	Compare against a threshold (e.g., $50).
4.	If exceeded, publish an SNS alert with the current spend.
5.	Print the retrieved amount for logging.
4.	EventBridge: Schedule daily.
5.	Testing: Trigger manually with a low threshold (e.g., $0.01) to force an alert.
6.	Discussion point: Mention AWS Budgets as the managed alternative and when custom Lambda logic wins (per-service breakdowns, Slack/Teams delivery, anomaly logic).
