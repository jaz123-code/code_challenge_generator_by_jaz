from fastapi import APIRouter, Depends, HTTPException, status,Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import (get_challenge_quota, reset_quota_if_needed, create_challenge_quota, get_user_challenges,create_challenge)
from ..utils import authenticate_and_get_user_details
from ..database.models import ChallengeQuota, Challenge
from ..database.models import get_db
import json
from datetime import datetime
from ..ai_generator import generate_mcq_challenge

router= APIRouter()
class ChallengeRequest(BaseModel):
    difficulty: str
class config:
    json_schema_extra={"example":{
        "difficulty":"easy"
    }}


@router.post("/generate-challenge")
async def generate_challenge(request: Request, challenge_request: ChallengeRequest, db: Session = Depends(get_db)):
    try:
        user_details = authenticate_and_get_user_details(request)
        user_id = user_details["user_id"]
        quota = get_challenge_quota(db, user_id)

        if not quota:
            quota = create_challenge_quota(db, user_id)

        quota = reset_quota_if_needed(db, quota)

        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Challenge quota exceeded")

        challenge_data = generate_mcq_challenge(challenge_request.difficulty)

        options_dict = challenge_data["options"]
        options_list = list(options_dict.values())
        
        answer_key = challenge_data["answer"]
        correct_answer_id = list(options_dict.keys()).index(answer_key)

        new_challenge = create_challenge(
            db=db,
            difficulty=challenge_request.difficulty,
            created_by=user_id,
            title=challenge_data["question"],
            options=json.dumps(options_list),
            correct_answer_id=correct_answer_id,
            explanation=challenge_data["explanation"]
        )

        quota.quota_remaining -= 1
        db.commit()

        return {
            "id": new_challenge.id,
            "difficulty": new_challenge.difficulty,
            "title": new_challenge.title,
            "options": json.loads(new_challenge.options),
            "correct_answer_id": new_challenge.correct_answer_id,
            "explanation": new_challenge.explanation,
            "timestamp": new_challenge.date_created.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@router.get("/my-history")
async def my_history(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    user_id= user_details["user_id"]
    challenges= get_user_challenges(db, user_id)
    return {"challenges": challenges}
@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    user_id= user_details["user_id"]
    quota= get_challenge_quota(db, user_id)
    quota= reset_quota_if_needed(db, quota)
    return quota
    

  


