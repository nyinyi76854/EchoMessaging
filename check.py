import yagmail

# Set up yagmail for sending email
sender_email = "messagingecho@gmail.com"
password = "zlqxukzxynmxkorz"
recipient_email = "nyinyilinnhtet399@gmail.com"
verification_code = "123456"  # Example verification code

# Initialize yagmail SMTP client
yag = yagmail.SMTP(sender_email, password)

try:
    # Send email with verification code
    yag.send(
        to=recipient_email,
        subject="Your Verification Code",
        contents=f"Your verification code is: {verification_code}"
    )
    print(f"Verification code sent to {recipient_email}")
except Exception as e:
    print(f"Failed to send email: {e}")
