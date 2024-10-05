from typing import List, Dict
from ollama import Client

class Assistant:
    def __init__(self, 
                 host = 'http://localhost:11434', 
                 model = "llama3.2:3b",
                 system_prompt = "You are a helpful assistant."
                 ):
        self.client = Client(host=host)
        self.model = model
        self.system_prompt = system_prompt
        
    def get_stream_from_history(self, chat_hx_list: List[Dict[str, str]]):
        # Getting Stream Generator Object
        stream = self.client.chat(model=self.model, stream=True,messages=chat_hx_list)
        return stream
        
    def get_stream(self, user_text: str):
        self.user_text = user_text
        # Getting Stream Generator Object
        stream = self.client.chat(model=self.model, 
                                stream=True,
                                messages=[
                                    {"role": "system", "content": "You are a helpful radiology assistant."},
                                    {"role": "user", "content": self.user_text}
                            ]
                            )
        return stream
 