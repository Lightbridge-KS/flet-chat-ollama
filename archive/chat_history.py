from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ChatHistory:
    role: str
    content: str

class ChatHistoryList:
    def __init__(self, chats: List[ChatHistory] = None):
        # Initialize with an empty list or provided list of ChatHistory objects
        self.chats = chats if chats else []

    def append(self, chat_dict: Dict[str, str]):
        # Check if the dictionary contains the required keys
        if 'role' in chat_dict and 'content' in chat_dict:
            # Convert dictionary to ChatHistory and append to the list
            chat_history = ChatHistory(**chat_dict)
            self.chats.append(chat_history)
        else:
            raise ValueError("Dictionary must contain 'role' and 'content' keys")
    
    def to_dict(self):
        return [chat_hx.__dict__ for chat_hx in self.chats]
    
    def __repr__(self):
        # Customize the string representation to show the internal list of ChatHistory objects
        return repr(self.chats)
    