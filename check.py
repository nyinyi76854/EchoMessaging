import yagmail
import firebase_admin
from firebase_admin import credentials, firestore
import random
import time
from datetime import datetime, timedelta

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccount.json")  # Firebase credentials file
firebase_admin.initialize_app(cred)
db = firestore.client()

# Set up yagmail for sending email
sender_email = "messagingecho@gmail.com"
password = "zlqxukzxynmxkorz"
yag = yagmail.SMTP(sender_email, password)

# Function to generate a random 6-digit verification code
def generate_code():
    return str(random.randint(100000, 999999))

# Function to send email
def send_verification_email(email, code):
    try:
        yag.send(
            to=email,
            subject="Your Verification Code",
            contents=f"Your verification code is: {code}"
        )
        print(f"Verification code sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

# Continuously check for new users to send verification codes
while True:
    try:
        # Get the current time and calculate 2 minutes ago
        now = datetime.utcnow()
        two_minutes_ago = now - timedelta(minutes=2)

        # Query users with timestamp within the last 2 minutes
        users_ref = db.collection('users')
        recent_users = users_ref.where('timestamp', '>=', two_minutes_ago).stream()

        for user in recent_users:
            user_data = user.to_dict()
            email = user_data.get('email')

            if email:
                verification_code = generate_code()

                # Save the verification code back to Firestore
                users_ref.document(user.id).update({
                    'verificationCode': verification_code
                })

                # Send the verification code via email
                send_verification_email(email, verification_code)
            else:
                print(f"No email found for user ID: {user.id}")

        # Wait for 30 seconds before checking again
        time.sleep(30)
    except Exception as e:
        print(f"Error during processing: {e}")
