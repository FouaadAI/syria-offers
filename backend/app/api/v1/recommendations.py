from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recommender import OfferRecommender
from app.schemas.offer import OfferResponse
from typing import List

router = APIRouter(prefix="/recommendations", tags=["التوصيات"])

recommender = OfferRecommender()

@router.get("/{user_id}", response_model=List[OfferResponse])
async def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    # إعادة تدريب النموذج بشكل سريع (في الإنتاج نستخدم تدريبًا دوريًا)
    recommender.fit(db)
    recommendations = recommender.recommend(user_id, db)
    return recommendations