import yagmail
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccount.json")  # Provide your Firebase credentials file
firebase_admin.initialize_app(cred)

# Set up yagmail for sending email
sender_email = "messagingecho@gmail.com"
password = "zlqxukzxynmxkorz"
yag = yagmail.SMTP(sender_email, password)

# Reference to the Firestore 'users' collection
db = firestore.client()
users_ref = db.collection('users')

# Get all documents in the 'users' collection
docs = users_ref.stream()

# Loop through all documents in 'users' collection
for doc in docs:
    user_data = doc.to_dict()
    
    # Get user data
    email = user_data.get('email')
    verification_code = user_data.get('verificationCode')

    # Ensure required fields are present
    if email and verification_code:
        try:
            # Send email with verification code
            yag.send(
                to=email,
                subject="Your Verification Code",
                contents=f"Your verification code is: {verification_code}"
            )
            print(f"Verification code sent to {email}")
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")
    else:
        print(f"Missing data for user with ID {doc.id}. Skipping.")
