from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Depends
from services.llm_service import generate_sales_summary
from services.email_service import send_summary_email
from middleware.auth import get_api_key
import pandas as pd
import io

router = APIRouter(tags=["Sales Analysis"])

@router.post("/upload")
async def upload_sales_data(
    file: UploadFile = File(...),
    email: str = Form(...),
    api_key: str = Depends(get_api_key)
):
    # Validate file type
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .csv or .xlsx file.")
    
    try:
        content = await file.read()
        
        # Parse data
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
            
        if df.empty:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")
            
        # Generate Summary
        summary = generate_sales_summary(df)
        
        # Send Email
        email_sent, email_error = send_summary_email(to_email=email, summary=summary)
        
        if not email_sent:
            return {"message": f"Summary generated successfully, but failed to send email. Reason: {email_error}", "summary": summary}
            
        return {"message": f"Summary generated and sent to {email} successfully."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
