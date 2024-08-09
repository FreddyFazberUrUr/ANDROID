import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.clock import Clock
import requests
from PIL import Image as PILImage
from io import BytesIO

class WaifuApp(App):
    def build(self):
        self.url = 'https://api.waifu.im/search'
        self.params = {'is_nsfw': False,
                       'included_tags': [],
                       'gif': False,
                       'excluded_files': []}

        self.layout = BoxLayout(orientation='vertical')
        self.image_widget = Image(size_hint_y=0.9)
        self.layout.add_widget(self.image_widget)

        button_layout = BoxLayout(size_hint_y=0.1)
        self.quit_button = Button(text='Выйти')
        self.next_button = Button(text='Дальше')
        self.back_button = Button(text='Назад')
        button_layout.add_widget(self.quit_button)
        button_layout.add_widget(self.next_button)
        button_layout.add_widget(self.back_button)
        self.layout.add_widget(button_layout)

        self.image_list = []
        self.current_image = None

        self.quit_button.bind(on_press=self.quit)
        self.next_button.bind(on_press=self.next_image)
        self.back_button.bind(on_press=self.prev_image)

        Clock.schedule_once(self.load_image, 0.1)

        return self.layout

    def load_image(self, dt):
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            data = response.json()
            img = PILImage.open(BytesIO(requests.get(data['images'][0]['url']).content)).resize((900, 800))
            self.current_image = img
            self.image_widget.texture = self.get_texture(img)
            self.image_list.append(self.current_image)
            self.params['excluded_files'].append(data['images'][0]['image_id'])
        else:
            img = PILImage.open('../../API_2/media/gosling.jpg')
            self.current_image = img
            self.image_widget.texture = self.get_texture(img)

    def get_texture(self, img):
        buf = BytesIO()
        img.save(buf, format='png')
        buf.seek(0)
        return kivy.core.image.Image(buf, ext='png').texture

    def next_image(self, instance):
        Clock.schedule_once(self.load_image, 0.1)

    def prev_image(self, instance):
        if self.image_list:
            self.image_list.pop()
            if self.image_list:
                self.current_image = self.image_list[-1]
                self.image_widget.texture = self.get_texture(self.current_image)
            else:
                self.load_image(None)

    def quit(self, instance):
        self.stop()


if __name__ == '__main__':
    WaifuApp().run()