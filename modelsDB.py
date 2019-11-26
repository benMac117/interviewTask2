from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import flask_marshmallow

Base = declarative_base()

# class for the recipe model
class Prediction(Base):
    __tablename__ = 'Prediction'
    id = Column(Integer, primary_key=True)
    totalVolume = Column(Float)
    volume4046 = Column(Float)
    volume4225 = Column(Float)
    volume4770 = Column(Float)
    totalBags = Column(Float)
    smallBags = Column(Float)
    largeBags = Column(Float)
    xLargeBags = Column(Float)
    avoType = Column(String(20))
    region = Column(String(20))
    epochTime = Column(Integer)
    month = Column(String(20))
    predictedPrice = Column(Float)

    def __init__(self, predictedPrice, totalVolume, volume4046, volume4225, volume4770, 
        totalBags, smallBags, largeBags, xLargeBags, avoType, region, epochTime, month):
        self.totalVolume = float(totalVolume)
        self.volume4046 = float(volume4046)
        self.volume4225 = float(volume4225)
        self.volume4770 = float(volume4770)
        self.totalBags = float(totalBags)
        self.smallBags = float(smallBags)
        self.largeBags = float(largeBags)
        self.xLargeBags = float(xLargeBags)
        self.avoType = avoType
        self.region = region
        self.epochTime = int(epochTime)
        self.month = month
        self.predictedPrice = float(predictedPrice)




# model schema - allow easy transport through JSON
class PredictionSchema(flask_marshmallow.Schema):
    class Meta:
        fields = ('id', 'totalVolume', 'volume4046', 'volume4225', 'volume4770', 
            'totalBags', 'smallBags', 'largeBags', 'xLargeBags', 'avoType', 'region', 
            'epochTime', 'month', 'predictedPrice')
