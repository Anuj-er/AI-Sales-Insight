import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
import os
import markdown

def send_summary_email(to_email: str, summary: str):
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not sender_email or not sender_password:
        print("Warning: SMTP credentials not provided. Skipping email delivery.")
        return False, "SMTP_EMAIL or SMTP_PASSWORD environment variables are not set."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Sales Insight Automator - Generated Summary"

    html_body = markdown.markdown(summary)
    
    # Wrap in a gorgeous "README" style CSS envelope
    styled_html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            line-height: 1.6;
            color: #24292f;
            background-color: #f6f8fa;
            padding: 20px;
          }}
          .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(27,31,35,0.04);
          }}
          h1, h2, h3 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
            border-bottom: 1px solid #d0d7de;
            padding-bottom: 0.3em;
          }}
          h1 {{ font-size: 2em; }}
          h2 {{ font-size: 1.5em; }}
          p {{ margin-top: 0; margin-bottom: 16px; }}
          ul, ol {{ padding-left: 2em; margin-bottom: 16px; }}
          li {{ margin-top: 0.25em; }}
          strong {{ font-weight: 600; }}
          blockquote {{
            padding: 0 1em;
            color: #57606a;
            border-left: 0.25em solid #d0d7de;
            margin: 0 0 16px 0;
          }}
          .header {{
            text-align: center;
            margin-bottom: 30px;
          }}
          .header-title {{
            background: linear-gradient(90deg, #0969da, #2da44e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 28px;
            font-weight: 800;
            border: none;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1 class="header-title">Sales Insight Automator</h1>
            <p style="color: #57606a;">Automated Executive Report</p>
          </div>
          {html_body}
          <hr style="height: 1px; background-color: #d0d7de; border: none; margin-top: 40px; margin-bottom: 20px;" />
          <p style="text-align: center; font-size: 12px; color: #8c959f;">Generated securely via Groq Llama-3.1-8b.</p>
        </div>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(styled_html, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True, None
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False, str(e)
