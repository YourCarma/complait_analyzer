from loguru import logger

from  utils import fetch_data

class GeolocationFinder:
    __slots__ = ("GEOLOCATION_FINDER_URL", )
    
    def __init__(self):
        self.GEOLOCATION_FINDER_URL = "http://ip-api.com/json/"
        
    async def get_geolocation(self, ip: str) -> str:
        try:
            payload = self.GEOLOCATION_FINDER_URL + ip
            result = await fetch_data(url=payload)
            logger.debug(
                f"Определенная геолокация: {result}"
            )
            return result
        except Exception as e:
            raise e
        
        