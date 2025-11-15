from fastapi import APIRouter, Request, Depends,HTTPException
from ..database.models import get_db
from ..database.db import create_challenge_quota
from svix.webhooks import Webhook, WebhookVerificationError
import os
import json
from dotenv import load_dotenv
load_dotenv()


router=APIRouter()

@router.post("/clerk")
async def handle_user_created(request: Request, db=Depends(get_db)):
    Webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
    if not Webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    body = await request.body()
    payload = body.decode('utf-8')
    header=dict(request.headers)
    try:
        wh = Webhook(Webhook_secret)
        event = wh.verify(payload, header)
        data=json.loads(event.data)
        if data.get("type")!="user.created":
            raise HTTPException(status_code=400, detail="Invalid event type")
        user_data=data.get("data",{})
        user_id=user_data.get("id")

        create_challenge_quota(db, user_id)
        return {"status":"success"}
    except WebhookVerificationError as e:
        logging.error(f"Webhook verification error: {e}")
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    
