from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix import image

#Builder.load_file('test_5.kv')

Window.size = (405, 720)

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class CustomPopup(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class MainWidget(BoxLayout):
    def load_dialog(self):
        content = CustomPopup(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title='Load file', content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    # delete popup
    def dismiss_popup(self):
        self._popup.dismiss()

    # load 
    def load(self, load_path):
        self.dismiss_popup()
        self.ids.label1.text = load_path[0]
        self.set_img(load_path[0])

    def set_img(self, path):
        self.ids.input_img.source = path

class MyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    MyApp().run()