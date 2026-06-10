import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.offer import Offer
from datetime import timedelta
class OfferRecommender:
    def __init__(self):
        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.offers_matrix = None
        self.offer_ids = []

    def fit(self, db: Session):
        """تدريب النموذج على بيانات الحجوزات الحالية"""
        bookings = db.query(Booking).all()
        if not bookings:
            return

        # بناء DataFrame من الحجوزات
        data = []
        for b in bookings:
            data.append({'user_id': b.user_id, 'offer_id': b.offer_id, 'count': 1})
        df = pd.DataFrame(data)

        if df.empty:
            return

        # إنشاء مصفوفة المستخدم × العرض
        matrix = df.pivot_table(index='user_id', columns='offer_id', values='count', fill_value=0)
        self.offer_ids = list(matrix.columns)
        self.offers_matrix = matrix.values

        if len(self.offers_matrix) > 1:
            self.model.fit(self.offers_matrix)

    def recommend(self, user_id: int, db: Session, n_recommendations: int = 4):
        # Zuerst kollaboratives Filtern versuchen
        if self.offers_matrix is not None and len(self.offers_matrix) > 1:
            try:
                user_idx = list(self.offers_matrix.index).index(user_id)
                distances, indices = self.model.kneighbors([self.offers_matrix[user_idx]], n_neighbors=min(3, len(self.offers_matrix)))
                neighbor_ids = list(self.offers_matrix.index[indices[0]])
                user_offers = set(self.offers_matrix.loc[user_id][self.offers_matrix.loc[user_id] > 0].index)
                recommended_offer_ids = set()
                for neighbor in neighbor_ids:
                    neighbor_offers = set(self.offers_matrix.loc[neighbor][self.offers_matrix.loc[neighbor] > 0].index)
                    recommended_offer_ids.update(neighbor_offers - user_offers)
                recommended_offer_ids = list(recommended_offer_ids)[:n_recommendations]
                if recommended_offer_ids:
                    offers = db.query(Offer).filter(Offer.id.in_(recommended_offer_ids), Offer.is_active == True, Offer.approved == True).all()
                    if offers: return offers
            except:
                pass
        # Fallback: Trending (nach Buchungen in den letzten 30 Tagen)
        trending = db.query(Offer).join(Booking, Booking.offer_id == Offer.id)\
                    .filter(Offer.is_active == True, Offer.approved == True, Booking.created_at >= func.now() - timedelta(days=30))\
                    .group_by(Offer.id).order_by(func.count(Booking.id).desc()).limit(n_recommendations).all()
        if not trending:
            # Wenn gar nichts, einfach neueste aktive Angebote
            trending = db.query(Offer).filter(Offer.is_active == True, Offer.approved == True).order_by(Offer.created_at.desc()).limit(n_recommendations).all()
        return trending