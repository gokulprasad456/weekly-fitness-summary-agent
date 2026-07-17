
import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('FitnessLog1')

workouts = [
    {"type": "Running", "duration_min": 30, "calories": 320, "steps": 8500, "notes": "Morning run, felt great"},
    {"type": "Rest", "duration_min": 0, "calories": 0, "steps": 4200, "notes": "Active recovery, light walking"},
    {"type": "Strength", "duration_min": 45, "calories": 280, "steps": 6100, "notes": "Upper body focus"},
    {"type": "Yoga", "duration_min": 40, "calories": 150, "steps": 3800, "notes": "Flexibility and mobility"},
    {"type": "Running", "duration_min": 35, "calories": 370, "steps": 9200, "notes": "Interval training"},
    {"type": "HIIT", "duration_min": 25, "calories": 310, "steps": 7600, "notes": "High intensity circuit"},
    {"type": "Rest", "duration_min": 0, "calories": 0, "steps": 5100, "notes": "Weekend rest day"},
]

print("Seeding Fitness Data to DynamoDB...")

for i, workout in enumerate(workouts):
    date = (datetime.now() - timedelta(days=6 - i)).strftime('%Y-%m-%d')
    table.put_item(Item={
        'user_id': 'gokulprasad',
        'date': date,
        'workout_type': workout['type'],
        'duration_min': workout['duration_min'],
        'calories': workout['calories'],
        'steps': workout['steps'],
        'notes': workout['notes']
    })
    print(f"  Added: {date} | {workout['type']} | {workout['steps']} steps")

print(f"Done! {len(workouts)} days of data added.")

