"""
Message with Stream
"""
    
from dataclasses import dataclass
from typing import Generator
import flet as ft

from _utils import get_initials, get_avatar_color

# DataClasses
@dataclass
class MessageStatic:
    user_name: str
    text: str

@dataclass
class MessageStream:
    user_name: str
    ai_stream: Generator[str, None, None]

@dataclass
class MessageLogin(MessageStatic):
    pass

@dataclass
class MessageUser(MessageStatic):
    pass

# ChatMessage with Streaming

class ChatMessageStream(ft.ResponsiveRow):
    """ChatMessage with Streaming for AI"""
    
    def __init__(self, message: MessageStream):
        super().__init__()
        self.message = message
        self.circle_avatar = ft.CircleAvatar(
            content=ft.Text(self.get_initials(self.message.user_name)),
            color=ft.colors.WHITE,
            bgcolor=self.get_avatar_color(self.message.user_name),
        )
        
        self.msg_bubble = ft.Container(
                                #   ft.Text(self.message.text, selectable=True),
                                ft.Markdown(
                                        "", selectable=True
                                ),
                                bgcolor=ft.colors.GREEN_200,
                                theme_mode=ft.ThemeMode.LIGHT,
                                border_radius=10,
                                margin=10,
                                padding=10,
        )
        self.controls = [
                ft.Column(col=1, controls=[self.circle_avatar]),
                ft.Column(col=10,
                    controls = [
                        ft.Text(self.message.user_name, weight="bold"),
                        self.msg_bubble
                    ],
                    tight=True,
                    spacing=5,
                )
            ]
        self.vertical_alignment = ft.CrossAxisAlignment.START
        
    def set_chat_msg(self, msg):
        self.msg_bubble.content.value += msg
        self.msg_bubble.update()
        
    @staticmethod
    def get_initials(user_name: str):
        return get_initials(user_name)

    @staticmethod
    def get_avatar_color(user_name: str):
        return get_avatar_color(user_name)


# Static Chat Message

class ChatMessageStatic(ft.ResponsiveRow):
    """Static ChatMessage for Human"""
    
    def __init__(self, message: MessageUser):
        super().__init__()
        self.message = message
        
        self.circle_avatar = ft.CircleAvatar(
            content=ft.Text(self.get_initials(self.message.user_name)),
            color=ft.colors.WHITE,
            bgcolor=self.get_avatar_color(self.message.user_name),
        )
        self.msg_bubble = ft.Container(
                                #   ft.Text(self.message.text, selectable=True),
                                ft.Markdown(
                                        self.message.text, selectable=True
                                ),
                                bgcolor=ft.colors.BLUE_200,
                                theme_mode=ft.ThemeMode.LIGHT,
                                border_radius=10,
                                margin=10,
                                padding=10,
                    )
        
        self.controls = [
                ft.Column(col=10,
                    controls = [ft.Text(self.message.user_name, weight="bold"), self.msg_bubble],
                    tight=True,
                    spacing=5, 
                    horizontal_alignment = ft.CrossAxisAlignment.END
                ),
                ft.Column(col=1, controls=[self.circle_avatar])
            ]
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.alignment = ft.MainAxisAlignment.END
        
    @staticmethod
    def get_initials(user_name: str):
        return get_initials(user_name)
        
    @staticmethod
    def get_avatar_color(user_name: str):
        return get_avatar_color(user_name)    
    
