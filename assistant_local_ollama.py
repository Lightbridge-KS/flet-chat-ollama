from ollama import Client

client = Client(host='http://localhost:11434')
model = "llama3.2:3b"


class Assistant:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
    def get_stream(self, user_text):
        self.user_text = user_text
        
        # [TODO] Implement Memory System (Generator object can only use once, there is no other way)
        
        while True:
            # Getting Stream Generator Object
            stream = client.chat(model=model, 
                                 stream=True,
                                 messages=[{"role": "user", "content": self.user_text}]
                                )
            return stream
        
    def get_response(self, user_text):
        self.user_text = user_text
        
        
        while True:
            # Storing the user question in the messages list
            self.messages.append({"role": "user", "content": self.user_text})
            
            # Getting Stream Generator Object
            stream = client.chat(model=model, 
                                stream=True,
                                messages=self.messages
                                )
            token_ls = []
            
            for chunk in stream:
                msg = chunk["message"]["content"]
                print(msg, end='', flush=True)
                token_ls.append(msg)
            
            response_str = "".join(token_ls)
            
            # Appending the generated response so that AI remembers past responses
            self.messages.append({
                "role":"assistant", "content": response_str               
            })
            return response_str


if __name__ == "__main__":
    a1 = Assistant()
    
    st = a1.get_stream("Hello, My name is Bob.")
    
    for chunk in st:
        print(chunk['message']['content'], end='', flush=True)
