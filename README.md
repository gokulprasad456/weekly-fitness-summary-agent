# 🏋️ Weekly Fitness Summary Agent

An autonomous AI-powered agent that generates personalized weekly fitness reports — built for the AWS Builder Weekend Challenge (July 2026).

## 🎯 What It Does

Every Monday at 6:00 AM IST, this agent automatically:

1. ⏰ Wakes up via EventBridge Scheduler (no human interaction)
2. 📊 Fetches the last 7 days of fitness data from DynamoDB
3. 🤖 Sends data to Amazon Bedrock (Nova Lite) to generate a personalized coach's report
4. 📧 Emails the beautiful HTML report via Amazon SES

**You never open it. The report is waiting when you wake up.**

---

## 🏗️ Architecture

EventBridge Scheduler (cron: Monday 6 AM IST) │ ▼ AWS Lambda (Python 3.12) │ ├──► DynamoDB (Read fitness data) ├──► Amazon Bedrock Nova Lite (Generate AI report) └──► Amazon SES (Send email)


---

## ☁️ AWS Services Used

| Service | Purpose | Free Tier |
|---------|---------|-----------|
| Amazon EventBridge Scheduler | Weekly cron trigger (Monday 6 AM IST) | ✅ 14M invocations/month |
| AWS Lambda | Agent orchestration (Python 3.12) | ✅ 1M requests/month |
| Amazon DynamoDB | Fitness data storage | ✅ 25 GB storage |
| Amazon Bedrock (Nova Lite) | AI-powered report generation | ✅ Free tier credits |
| Amazon SES | Email delivery | ✅ 62,000 emails/month |
| AWS IAM | Least-privilege permissions | ✅ Free |
| Amazon CloudWatch | Logging & monitoring | ✅ 5 GB logs |

---

## 📧 Sample Output

The agent delivers an HTML email containing:

- 📊 **Stats at a Glance** — Total workouts, steps, calories, best day
- 📈 **Weekly Trends** — What improved, what dipped
- 💬 **Coach's Take** — Personalized encouragement
- 🎯 **Challenge for Next Week** — One achievable goal
- 💡 **Quick Tip** — Relevant health/fitness tip

---

## 🚀 Setup Instructions

### Prerequisites

- AWS Account (Free Tier eligible)
- Email verified in Amazon SES
- Amazon Bedrock Nova Lite model access enabled

### Step-by-Step

1. **Create DynamoDB Table**
   - Table name: `FitnessLog1`
   - Partition key: `user_id` (String)
   - Sort key: `date` (String)
   - Billing: On-demand

2. **Seed Sample Data**
   - Run `seed_data.py` locally or in AWS CloudShell
   - Adds 7 days of fitness entries

3. **Enable Bedrock Model Access**
   - AWS Console → Bedrock → Model access
   - Enable Amazon Nova Lite

4. **Create IAM Role**
   - Role name: `FitnessAgentLambdaRole`
   - Attach policy from `iam-permissions-policy.json`

5. **Create Lambda Function**
   - Function name: `WeeklyFitnessSummaryAgent`
   - Runtime: Python 3.12
   - Timeout: 90 seconds
   - Code: `lambda_function.py`

6. **Verify Email in SES**
   - Verify sender/recipient email in Amazon SES

7. **Create EventBridge Schedule**
   - Schedule: `cron(30 0 ? * MON *)`
   - Timezone: Asia/Kolkata
   - Target: Lambda function `WeeklyFitnessSummaryAgent`

8. **Test**
   - Invoke Lambda manually → Check email inbox

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `lambda_function.py` | Main agent code (Lambda handler) |
| `seed_data.py` | Populates DynamoDB with 7 days of sample fitness data |
| `iam-permissions-policy.json` | IAM permissions for Lambda role |
| `eventbridge-scheduler-config.json` | Scheduler configuration reference |
| `README.md` | This file |

---

## 💰 Cost

**$0/month** — All services operate within AWS Free Tier limits.

| Service | Free Tier Limit | Agent Usage |
|---------|-----------------|-------------|
| Lambda | 1M requests/month | ~4 requests/month |
| DynamoDB | 25 GB + 25 RCU | < 1 KB |
| Bedrock Nova Lite | Free tier credits | ~4 calls/month |
| SES | 62,000 emails/month | ~4 emails/month |
| EventBridge | 14M invocations/month | ~4/month |

---

## 🔮 Future Enhancements

- Connect real fitness tracker APIs (Strava, Google Fit, Apple Health)
- Add week-over-week trend comparison
- Include visual charts in the email
- Add SNS notifications for milestone achievements
- Multi-user support with Cognito authentication

---

## 🏆 Built For

**AWS Builder Center Weekend Challenge:** "Build an Always-On Agent"

📅 July 17–20, 2026

---

## 👤 Author

**Gokul Prasad**

---

## 🏷️ Tags
