import os
import boto3
from datetime import date

ce = boto3.client("ce")
sns = boto3.client("sns")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
THRESHOLD = float(os.environ["COST_THRESHOLD"])


def lambda_handler(event, context):

    today = date.today()
    start_date = today.replace(day=1)

    response = ce.get_cost_and_usage(
        TimePeriod={
            "Start": start_date.strftime("%Y-%m-%d"),
            "End": today.strftime("%Y-%m-%d")
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"]
    )

    amount = float(
        response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    )

    print(f"Current Month-to-Date Cost: ${amount:.2f}")

    if amount >= THRESHOLD:

        subject = "AWS Daily Cost Alert"

        message = f"""
AWS Cost Threshold Exceeded

Current Spend : ${amount:.2f}

Threshold     : ${THRESHOLD:.2f}

Please review your AWS Billing Dashboard.

Generated Automatically by AWS Lambda.
"""

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )

        print("Alert sent successfully.")

    return {
        "statusCode": 200,
        "CurrentCost": amount
    }
