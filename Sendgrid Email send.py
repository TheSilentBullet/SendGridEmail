# Importing the dependencies
import os
import sendgrid
from sendgrid.helpers.mail import *

# Initialize SendGrid client with API key
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

# Recipients list
recipients = [
    {"first_name": "Alex", "email": "alex@yahoo.com"},
    {"first_name": "Daniel", "email": "daniel@gmail.com.com"}
]

# Attachment file path
attachment_file_path = "/path/to/your/attachment.pdf"

# Iterate over recipients
for recipient in recipients:
    # Prepare personalization
    personalization = {
        "to": [{"email": recipient["email"], "type": "to"}],
        "dynamic_template_data": {"first_name": recipient["first_name"]},
        "template_id": "your_template_id"
    }
    
    # Read attachment
    with open(attachment_file_path, 'rb') as attachment_file:
        attachment = Attachment(
            filename=attachment_file.name,
            filetype=FileType.CUSTOM,
            disposition=Disposition.Attachment,
            content=attachment_file.read(),
            content_type="application/pdf",
            name=attachment_file.name
        )
    
    # Prepare email
    from_email = Email("from_email@example.com")
    to_email = To(recipient["email"])
    subject = f"Hello {recipient['first_name']}!"
    content = Content("text/plain", "Please see the PDF for more details.")
    mail = Mail(from_email, subject, to_email, content, attachments=[attachment])
    
    # Add personalization
    mail.add_personalization(personalization)
    
    # Send email
    response = sg.client.mail.send.post(request_body=mail.get())
    print(f"Email sent to {recipient['email']}: {response.status_code}")