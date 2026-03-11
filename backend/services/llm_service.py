from groq import Groq
import os
import pandas as pd

def generate_sales_summary(df: pd.DataFrame) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: Groq API key not configured."
    
    client = Groq(api_key=api_key)
    
    # Calculate some basic metrics to give the LLM context without sending too big of a payload
    total_revenue = df['Revenue'].sum() if 'Revenue' in df.columns else "N/A"
    total_units = df['Units_Sold'].sum() if 'Units_Sold' in df.columns else "N/A"
    
    prompt = f"""
You are a senior sales analyst. Summarize the following sales data into a professional narrative for executive leadership.
Total Revenue: {total_revenue}
Total Units Sold: {total_units}

Dataset Preview (First 50 rows):
{df.head(50).to_csv(index=False)}

Please provide a concise, insightful summary focusing on key trends, best-performing categories, and any noticeable patterns. Keep it professional.
"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return f"Failed to generate summary: {str(e)}"
