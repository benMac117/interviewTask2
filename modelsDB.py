from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import flask_marshmallow

Base = declarative_base()

# class for the recipe model
class Prediction(Base):
    __tablename__ = 'Prediction'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name


# model schema - allow easy transport through JSON
class PredictionSchema(flask_marshmallow.Schema):
    class Meta:
        fields = ('id', 'name')