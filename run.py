from kivy.lang import Builder
from kivymd.app import MDApp
import os
import django
import subprocess

KV = '''
MDScreen:
    MDTopAppBar:
        type: "top"
        size_hint_x: 1
        pos_hint: {"center_x": .5, "center_y": 0.95}
        left_action_items: []
        right_action_items: [["account-circle-outline", lambda x: None]]
        title: "AVC Admin"
    Image:
        source: "static/assets/avc.png"
        size_hint: None, None
        size: 80, 80 
        pos_hint: {"left": 1, "center_y": 0.95,"center_x":0.1}
    BoxLayout:
        orientation: 'horizontal'
        # Left section for the button
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.5
            MDRectangleFlatButton
                text : "start server"
                pos_hint : {"center_x":.5,"center_y":.9}
                on_release : app.run_server()
            MDRectangleFlatButton
                text : "stop server"
                pos_hint : {"center_x":.5,"center_y":.5}
                on_release : app.stop_server()       
        # Right section for the label
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.5
            MDLabel:
                id: label
                text: "start the server"
                halign: "center"
                valign: "center"
                theme_text_color: "Primary"     
'''

class MainApp(MDApp):
    server_process = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        return Builder.load_string(KV)

    def run_server(self):
        if self.server_process is None:  
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback.settings')
            django.setup()
            self.root.ids.label.text = "server is now running"
            self.server_process = subprocess.Popen(["python", "manage.py", "runserver"])

    def stop_server(self):
        if self.server_process is not None:
            self.root.ids.label.text = "server is now stopped"
            self.server_process.terminate()  
            self.server_process = None  

MainApp().run()
