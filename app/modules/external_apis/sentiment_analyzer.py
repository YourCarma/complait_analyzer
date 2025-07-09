from loguru import logger
import json

from  utils import post_data
from settings import settings

class SentimentAnalyzer:
    __slots__ = ("ANALYZER_URL", )
    
    def __init__(self):
        self.ANALYZER_URL = "https://api.apilayer.com/sentiment/analysis"
        
    async def get_sentimentality(self, text: str) -> str:
        try:
            headers = {
                "apikey": settings.API_LAYER_SENTIMENT_KEY
            }
            payload = text.encode("utf-8")
            result = await post_data(url=self.ANALYZER_URL, headers=headers, data=payload)
            logger.debug(
                f"Определенная тональность: {result}"
            )
            return result
        except Exception as e:
            raise e
        
        