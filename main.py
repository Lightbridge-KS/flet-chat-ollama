from dataclasses import dataclass
import time
import flet as ft

from message import ChatMessage
from message_st import Message, MessageStream, ChatMessageStream
# from assistant_local_openai import Assistant
from assistant_local_ollama import Assistant

# Generator function that yields each letter from "HELLO" with a delay
def hello_generator():
    import time
    word = "HELLO"
    for letter in word:
        yield letter
        time.sleep(0.5)

class ChatView(ft.ListView):
    def __init__(self):
        super().__init__()
        self.spacing = 10
        self.auto_scroll = True
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS



def main(page: ft.Page):
    
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    # Title
    page.title = "LLM Chat"
    # page.window.min_width = 450
    # page.window.width = 550
    # page.window.min_height = 500
    # page.window.height = 600
    
    # App Bar
    page.appbar = ft.CupertinoAppBar(
        bgcolor=ft.colors.SURFACE_VARIANT,
        middle=ft.Text("LLM Chat", weight=ft.FontWeight.BOLD),
    )
    
    chat = ChatView()
    


    def on_message(message: Message | MessageStream):
        match message.message_type:
            case "chat_message":
                m = ChatMessage(message)
                chat.controls.append(m)
            case "chat_message_stream":
                # [TODO] Implement real one
                m = ChatMessageStream(message)
                chat.controls.append(m)
                page.update()
                
                for chunk in message.ai_stream:
                    text_token = chunk["message"]["content"]
                    m.set_chat_msg(text_token)
                    page.update()  # Update the page to reflect the changes in real-time

                
            case "login_message":
                m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
                chat.controls.append(m)
        
        page.update()

    page.pubsub.subscribe(on_message)


    def send_message_click(e):
        if new_message.value != "":
            
            ## Send User Message
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            ### Clear the content in message box
            human_msg = new_message.value
            new_message.value = ""
            
            ## Fetching the AI response (Generator Object)
            ai_stream = assistant.get_stream(str(human_msg))
            # ai_stream_test = hello_generator()
            time.sleep(0.25)
            
            ## Sent AI Message 
            page.pubsub.send_all(
                MessageStream(
                "AI", 
                ai_stream, # ai_stream A Generator 
                message_type="chat_message_stream"
                )
            )

            
            
            new_message.focus()
            page.update()


    def join_click(e):
        if not user_name.value:
            user_name.error_text = "Name cannot be blank!"
            user_name.update()
        else:
            page.session.set("user_name", user_name.value)
            page.dialog.open = False
            new_message.prefix =ft.Text(" " * 2)
            page.pubsub.send_all(
                Message(
                    user_name=user_name.value,
                    text=f"{user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()
    
    user_name = ft.TextField(
        label="Enter your name",
        autofocus=True,
        on_submit=join_click,
    )
    
    # Alert Dialog
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([user_name], tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_click)],
        actions_alignment=ft.MainAxisAlignment.END, # "end"
    )
    
    # Creating LLM Assistance
    assistant = Assistant()

    # New MSG box at the bottom
    new_message = ft.TextField(
        hint_text="Message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=10, # 5
        border_radius=30,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add Everything !!
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    on_click=send_message_click,
                ),
            ]
        ),
    )

ft.app(target=main)