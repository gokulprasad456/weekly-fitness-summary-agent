
import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
ses = boto3.client('ses', region_name='us-east-1')

USER_ID = 'gokulprasad'
EMAIL = 'cgokulprasad@gmail.com'
TABLE_NAME = 'FitnessLog1'


def get_weekly_data():
    table = dynamodb.Table(TABLE_NAME)
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(USER_ID) &
                              Key('date').between(
                                  week_ago.strftime('%Y-%m-%d'),
                                  today.strftime('%Y-%m-%d')
                              )
    )
    return response['Items']


def generate_summary(fitness_data):
    data_text = json.dumps(fitness_data, indent=2, default=str)
    prompt = f"""You are a supportive fitness coach. Analyze this week's fitness data and write a weekly summary report.

Include:
1. Stats at a Glance - total workouts (non-rest days), total steps, total calories, avg daily steps, best day
2. Trends - what improved, what dipped
3. Coach's Take - 2-3 sentences of personalized encouragement
4. Challenge for Next Week - one specific achievable goal
5. Quick Tip - one short health tip relevant to their routine

Tone: friendly, motivating, concise.

Data:
{data_text}

Today: {datetime.now().strftime('%A, %B %d, %Y')}"""

    response = bedrock.invoke_model(
        modelId='amazon.nova-lite-v1:0',
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            "messages": [{"role": "user", "content": [{"text": prompt}]}],
            "inferenceConfig": {"maxTokens": 1024, "temperature": 0.7}
        })
    )
    result = json.loads(response['body'].read())
    return result['output']['message']['content'][0]['text']


def send_email(summary):
    week_start = (datetime.now() - timedelta(days=7)).strftime('%b %d')
    week_end = datetime.now().strftime('%b %d, %Y')

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h1 style="color: #2c3e50;">Weekly Fitness Summary</h1>
            <p style="color: #888;">Week of {week_start} - {week_end}</p>
            <hr style="border: 1px solid #eee;">
            <div style="line-height: 1.8; color: #333; font-size: 15px;">
                {summary.replace(chr(10), '<br>')}
            </div>
            <hr style="border: 1px solid #eee;">
            <p style="color: #aaa; font-size: 11px;">Generated autonomously by your Fitness Summary Agent. Powered by AWS Lambda + Amazon Bedrock + EventBridge</p>
        </div>
    </body>
    </html>
    """

    ses.send_email(
        Source=EMAIL,
        Destination={'ToAddresses': [EMAIL]},
        Message={
            'Subject': {'Data': f'Weekly Fitness Summary ({week_start} - {week_end})'},
            'Body': {'Html': {'Data': html_body}}
        }
    )


def lambda_handler(event, context):
    print("Agent triggered!")

    print("Fetching weekly data...")
    data = get_weekly_data()
    if not data:
        print("No data found")
        return {'statusCode': 200, 'body': 'No data'}

    print(f"Found {len(data)} days of data")

    print("Generating AI summary with Bedrock...")
    summary = generate_summary(data)
    print("Summary generated successfully")

    print("Sending email...")
    send_email(summary)
    print("Email sent!")

    return {'statusCode': 200, 'body': json.dumps({'message': 'Summary sent!', 'days': len(data)})}

