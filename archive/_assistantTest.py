import os

class Assistant:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        
    def get_response(self, user_text):
        self.user_text = user_text
        while True:
            # if user says stop, then breaking the loop
            if self.user_text == "stop":
                break
            response_str = "Tester"
            print(response_str)
            return response_str
    

if __name__ == "__main__":
    a1 = Assistant()
    a1.get_response("Hello")
    