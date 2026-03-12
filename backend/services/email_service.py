import os
import httpx
import markdown

def send_summary_email(to_email: str, summary: str):
    api_key = os.getenv("RESEND_API_KEY")

    if not api_key:
        print("Warning: RESEND_API_KEY not set. Skipping email delivery.")
        return False, "RESEND_API_KEY environment variable is not set."

    html_body = markdown.markdown(summary)

    styled_html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
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

    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "from": f"Sales Insight Automator <{os.getenv('SENDER_EMAIL', 'onboarding@resend.dev')}>",
                "to": [to_email],
                "subject": "Sales Insight Automator - Generated Summary",
                "html": styled_html,
            },
            timeout=30,
        )
        if response.status_code == 200 or response.status_code == 201:
            return True, None
        else:
            error = response.json().get("message", response.text)
            print(f"Resend API error: {error}")
            return False, error
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False, str(e)

