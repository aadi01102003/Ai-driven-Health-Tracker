import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class FoodEntry(Base):
    __tablename__ = 'food_log'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    food = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fats = Column(Float, nullable=False)

class WeightEntry(Base):
    __tablename__ = 'weight_log'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    weight = Column(Float, nullable=False)

class DietaryPreferences(Base):
    __tablename__ = 'dietary_preferences'

    id = Column(Integer, primary_key=True)
    allergies = Column(JSON, nullable=True)
    restrictions = Column(JSON, nullable=True)
    preferred_cuisines = Column(JSON, nullable=True)
    disliked_ingredients = Column(JSON, nullable=True)
    meal_timing_preferences = Column(JSON, nullable=True)

class DataManager:
    def __init__(self):
        """Initialize DataManager with PostgreSQL connection"""
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")

        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_food_entry(self, food, calories, protein, carbs, fats):
        """Add a food entry to the food log"""
        entry = FoodEntry(
            date=datetime.now().date(),
            food=food,
            calories=float(calories),
            protein=float(protein),
            carbs=float(carbs),
            fats=float(fats)
        )
        self.session.add(entry)
        self.session.commit()

    def update_food_entry(self, index, food, calories, protein, carbs, fats):
        """Update an existing food entry"""
        entry = self.session.query(FoodEntry).filter(FoodEntry.id == index).first()
        if entry:
            entry.food = food
            entry.calories = float(calories)
            entry.protein = float(protein)
            entry.carbs = float(carbs)
            entry.fats = float(fats)
            self.session.commit()

    def get_todays_food_log(self):
        """Get today's food entries"""
        today = datetime.now().date()
        entries = self.session.query(FoodEntry).filter(FoodEntry.date == today).all()
        return [{
            'food': entry.food,
            'calories': entry.calories,
            'protein': entry.protein,
            'carbs': entry.carbs,
            'fats': entry.fats,
            'id': entry.id
        } for entry in entries]

    def add_weight_entry(self, weight):
        """Add a weight entry to the weight log"""
        entry = WeightEntry(
            date=datetime.now().date(),
            weight=float(weight)
        )
        self.session.add(entry)
        self.session.commit()

    def get_daily_totals(self):
        """Get total nutritional values for today"""
        today = datetime.now().date()
        entries = self.session.query(FoodEntry).filter(FoodEntry.date == today).all()
        return {
            'calories': sum(entry.calories for entry in entries),
            'protein': sum(entry.protein for entry in entries),
            'carbs': sum(entry.carbs for entry in entries),
            'fats': sum(entry.fats for entry in entries)
        }

    def get_weight_history(self):
        """Get weight history for plotting"""
        entries = self.session.query(WeightEntry).order_by(WeightEntry.date).all()
        return [{
            'date': entry.date,
            'weight': entry.weight
        } for entry in entries]

    def save_dietary_preferences(self, preferences):
        """Save or update dietary preferences"""
        pref = self.session.query(DietaryPreferences).first()
        if not pref:
            pref = DietaryPreferences(**preferences)
            self.session.add(pref)
        else:
            for key, value in preferences.items():
                setattr(pref, key, value)
        self.session.commit()

    def get_dietary_preferences(self):
        """Get saved dietary preferences"""
        pref = self.session.query(DietaryPreferences).first()
        if not pref:
            return {}
        return {
            'allergies': pref.allergies or [],
            'restrictions': pref.restrictions or [],
            'preferred_cuisines': pref.preferred_cuisines or [],
            'disliked_ingredients': pref.disliked_ingredients or [],
            'meal_timing_preferences': pref.meal_timing_preferences or {}
        }