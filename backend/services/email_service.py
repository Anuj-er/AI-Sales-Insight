import os
import httpx
import markdown

def send_summary_email(to_email: str, summary: str):
    api_key = os.getenv("RESEND_API_KEY")

    if not api_key:
        print("Warning: RESEND_API_KEY not set. Skipping email delivery.")
        return False, "RESEND_API_KEY environment variable is not set."

    html_body = markdown.markdown(summary)

    styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Sales Insight Report</title>
</head>
<body style="margin:0;padding:0;background-color:#f1f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">

  <!-- Outer wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f5f9;padding:40px 16px;">
    <tr>
      <td align="center">

        <!-- Card -->
        <table width="100%" style="max-width:640px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.07);">

          <!-- Header banner -->
          <tr>
            <td style="background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);padding:40px 48px 36px;text-align:center;">
              <p style="margin:0 0 12px;font-size:11px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#94a3b8;">Automated Executive Report</p>
              <h1 style="margin:0;font-size:26px;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">Sales Insight Automator</h1>
              <p style="margin:12px 0 0;font-size:13px;color:#64748b;">Generated on {__import__('datetime').datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </td>
          </tr>

          <!-- Divider accent -->
          <tr>
            <td style="height:4px;background:linear-gradient(90deg,#3b82f6,#06b6d4,#10b981);"></td>
          </tr>

          <!-- Body content -->
          <tr>
            <td style="padding:40px 48px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="
                    font-size:15px;
                    line-height:1.8;
                    color:#334155;
                  ">
                    <style>
                      .email-body h1,.email-body h2,.email-body h3{{
                        color:#0f172a;
                        font-weight:700;
                        margin:28px 0 12px;
                        line-height:1.3;
                      }}
                      .email-body h1{{font-size:22px;border-bottom:2px solid #e2e8f0;padding-bottom:10px;}}
                      .email-body h2{{font-size:18px;border-left:3px solid #3b82f6;padding-left:12px;}}
                      .email-body h3{{font-size:15px;color:#475569;}}
                      .email-body p{{margin:0 0 16px;}}
                      .email-body ul,.email-body ol{{margin:0 0 16px;padding-left:24px;}}
                      .email-body li{{margin-bottom:6px;}}
                      .email-body strong{{color:#0f172a;font-weight:600;}}
                      .email-body blockquote{{
                        margin:20px 0;
                        padding:16px 20px;
                        background:#f8fafc;
                        border-left:4px solid #3b82f6;
                        border-radius:0 8px 8px 0;
                        color:#475569;
                        font-style:italic;
                      }}
                      .email-body table{{width:100%;border-collapse:collapse;margin:16px 0;}}
                      .email-body th{{background:#f1f5f9;color:#0f172a;font-weight:600;padding:10px 14px;text-align:left;border:1px solid #e2e8f0;font-size:13px;}}
                      .email-body td{{padding:10px 14px;border:1px solid #e2e8f0;font-size:13px;color:#334155;}}
                      .email-body tr:nth-child(even) td{{background:#f8fafc;}}
                    </style>
                    <div class="email-body">{html_body}</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f8fafc;border-top:1px solid #e2e8f0;padding:24px 48px;text-align:center;">
              <p style="margin:0 0 6px;font-size:12px;color:#94a3b8;">This report was generated automatically by</p>
              <p style="margin:0 0 12px;font-size:13px;font-weight:600;color:#475569;">Sales Insight Automator</p>
              <p style="margin:0;font-size:11px;color:#cbd5e1;letter-spacing:1px;text-transform:uppercase;">Powered by Groq &middot; FastAPI &middot; Next.js</p>
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""

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

