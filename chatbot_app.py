from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests

class ChatBotApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.chat_history = Label(size_hint_y=0.8, text="Bem-vindo ao Chatbot!\n", halign='left', valign='top')
        self.chat_history.bind(size=self.chat_history.setter('text_size'))
        
        self.input_field = TextInput(size_hint_y=0.1, multiline=False)
        self.input_field.bind(on_text_validate=self.send_message)
        
        self.send_button = Button(text="Enviar", size_hint_y=0.1)
        self.send_button.bind(on_press=self.send_message)
        
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.input_field)
        self.layout.add_widget(self.send_button)
        
        return self.layout
    
    def send_message(self, instance):
        user_message = self.input_field.text.strip()
        if user_message:
            self.chat_history.text += f"\nVocê: {user_message}"
            self.input_field.text = ""
            
            try:
                response = requests.post("https://processos-ux.onrender.com/chat", json={"message": user_message})
                bot_reply = response.json().get("response", "Erro ao obter resposta.")
            except Exception as e:
                bot_reply = "Erro ao conectar com o servidor."
            
            self.chat_history.text += f"\nBot: {bot_reply}"  

if __name__ == "__main__":
    ChatBotApp().run()
