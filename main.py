from flask import Flask, jsonify
import requests
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize Flask app
app = Flask(__name__)

# Twilio Credentials (replace with your actual credentials)
TWILIO_SID = "ACdee47a8e25eecd7e200a595839065d52"
TWILIO_AUTH_TOKEN = "50258f2fde79384bcf649f83912ad872"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number
USER_WHATSAPP_NUMBER = "whatsapp:+917815861259"

# LeetCode username
LEETCODE_USERNAME = "gopi_kiran"

# Function to check LeetCode activity
def check_leetcode_activity():
    url = "https://leetcode.com/graphql/"
    headers = {"Content-Type": "application/json"}
    query = {
        "query": '''
        {
          matchedUser(username: "''' + LEETCODE_USERNAME + '''") {
            submitStatsGlobal {
              acSubmissionNum {
                count
              }
            }
          }
        }'''
    }

    response = requests.post(url, json=query, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        solved_today = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][-1]["count"]

        if solved_today>0:
            send_whatsapp_alert()
            return {"message": "No problem solved. WhatsApp alert sent!"}
        else:
            return {"message": "You have solved at least one problem today!"}
    else:
        return {"error": "Failed to fetch LeetCode data"}

# Function to send WhatsApp alert
def send_whatsapp_alert():
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body="You haven't solved a LeetCode problem today! Get back to coding! 🚀",
        from_=TWILIO_WHATSAPP_NUMBER,
        to=USER_WHATSAPP_NUMBER
    )
    print(f"WhatsApp Alert Sent! Message SID: {message.sid}")

# Set up daily scheduler (runs at 10 PM)
scheduler = BackgroundScheduler()
scheduler.add_job(check_leetcode_activity, "cron", hour=16, minute=55)
scheduler.start()

# Flask route to manually check
@app.route("/check", methods=["GET"])
def manual_check():
    return jsonify(check_leetcode_activity())

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
