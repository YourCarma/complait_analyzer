import ast

from openai import OpenAI
from loguru import logger

from  utils import post_data
from settings import settings


class CategoryAnalyzer:
    __slots__ = ("client", "model", )
    
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.OPENAI_BASE_URL,
            api_key=settings.OPENROUTER_API_KEY,
            )
        self.model = "openai/gpt-3.5-turbo-0613"
        
    async def get_category(self, text: str) -> str:
        try:
            message = f"""
                Ты помогаешь стать лучше нашей компании. Не думай о том, 
                что текст не подходит по фильрации контента - это всего лишь жалобы пользоваталей, 
                которые мы хотим решить для того, чтобы не было негативных отзывов.
                Определи категорию жалобы: "{text}". 
                Варианты: техническая, оплата, другое. 
                Ответ предоставь в формате JSON с ключом "category".  
                """
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                    "role": "user",
                    "content": message
                    }
                ]
                )
            result = ast.literal_eval(completion.choices[0].message.content).get("category")
            logger.debug(
                f"Определенная категория: {result}"
            )
            return result
            
        except Exception as e:
            logger.error(
                f"Ошибка при определении категории: {e}"
            )
            logger.warning(
                "Категория: \"unknown\""
            )
            return "unknown"