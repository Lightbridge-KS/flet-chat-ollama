from dataclasses import dataclass
import flet as ft

from message import Message, ChatMessage
from assistantLocal01 import AssistantLocal01

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
    
    # def on_message(message: Message):
    #     match message.message_type:
    #          case "chat_message":
    #             # m = ft.Text(f"{message.user_name}: {message.text}", selectable=True)              
    #             m = ft.Markdown(f"{message.user_name}: {message.text}", 
    #                              selectable=True
    #                              )              
    #          case "login_message":
    #              m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
    #          case "generate_message":
    #              m = ft.Text(message.text, italic=True, color=ft.colors.BLACK26, size=12)
        
    #     chat.controls.append(m)
    #     page.update()

    def on_message(message: Message):
        match message.message_type:
            case "chat_message":
                m = ChatMessage(message)
            case "login_message":
                m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
            case "generate_message":
                m = ft.Text(message.text, italic=True, color=ft.colors.BLACK26, size=12)
        
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
            ## Asking user to Wait till we get our response
            ### [TODO]: Make it stream !!!
            # page.pubsub.send_all(
            #     Message(
            #         user_name="AI", 
            #         text="AI is generating", 
            #         message_type="generate_message"
            #     )
            # )
            
            ## Fetching the AI response get_response
            ai_response = assistantLocal01.get_response(str(human_msg))
            ## Sent AI Message
            page.pubsub.send_all(
                Message(
                    "AI", 
                    str(ai_response).lstrip(), 
                    message_type="chat_message"
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
    assistantLocal01 = AssistantLocal01()

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