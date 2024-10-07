from typing import List, Dict
import openai
from openai import OpenAI


class Assistant:
    api_type = "openai"
    
    def __init__(self, 
                 host = 'http://localhost:11434/v1', 
                 model = "llama3.2:3b",
                 system_prompt = "You are a helpful assistant."
                 ):
        self.client = OpenAI(
        base_url=host,
        api_key="nokeyneeded"
        )
        self.model = model
        self.system_prompt = system_prompt
        
    def get_stream_from_history(self, chat_hx_list: List[Dict[str, str]]):
        # Getting Stream Generator Object
        stream = self.client.chat.completions.create(model=self.model, stream=True, messages=chat_hx_list)
        return stream
    
    def get_stream(self, user_text: str):
        # Getting Stream Generator Object
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_text}],
            stream=True
        )
        return stream
    
if __name__ == "__main__":
    a1 = Assistant()
    stream1 = a1.get_stream("Hello")
    for chunk in stream1:
        print(chunk.choices[0].delta.content, end="")