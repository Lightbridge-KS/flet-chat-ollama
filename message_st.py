"""
Message with Stream
"""
    
from dataclasses import dataclass
from typing import Generator
import flet as ft

@dataclass
class Message:
    user_name: str
    text: str | Generator[str, None, None]
    message_type: str

@dataclass
class MessageStream:
    user_name: str
    ai_stream: Generator[str, None, None]
    message_type: str


class ChatMessageStream(ft.UserControl):
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
        

    
    def set_chat_msg(self, msg):
        self.msg_bubble.content.value += msg
        self.msg_bubble.update()

    
    def build(self):  
            
        rr = ft.ResponsiveRow(
            controls = [
                ft.Column(col=1, controls=[self.circle_avatar]),
                ft.Column(col=10,
                    controls = [
                        ft.Text(self.message.user_name, weight="bold"),
                        self.msg_bubble
                    ],
                    tight=True,
                    spacing=5,
                )
            ],
            vertical_alignment = ft.CrossAxisAlignment.START,
        )
        
        return rr
    
    
    @staticmethod
    def get_initials(user_name: str):
        if user_name:
            return user_name[:1].capitalize()
        else:
            return "User"  # or any default value you prefer


    @staticmethod
    def get_avatar_color(user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
    
