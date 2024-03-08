from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
import pandas
import random

BACKGROUND_COLOR = (0.69, 0.87, 0.78, 1)  


class FlashyApp(App):
    def __init__(self, **kwargs):
        super(FlashyApp, self).__init__(**kwargs)
        self.learn_dict = {}
        try:
            data = pandas.read_csv("./data/words_to_learn.csv")
        except FileNotFoundError:
            original_data = pandas.read_csv("./data/french_words.csv")
            self.learn_dict = original_data.to_dict(orient="records")
        else:
            self.learn_dict = data.to_dict(orient="records")

        self.current_card = None
        self.flip_timer = None

    def build(self):
        root = BoxLayout(orientation='vertical', padding=50, spacing=10, background_color=BACKGROUND_COLOR)

        self.card_background = Image(source="./images/card_front.png")
        root.add_widget(self.card_background)

        self.card_title = Label(text="Title", font_size=40, italic=True)
        root.add_widget(self.card_title)

        self.card_word = Label(text="Word", font_size=30, italic=True)
        root.add_widget(self.card_word)

        button_layout = BoxLayout(orientation='horizontal', spacing=10)

        cross_btn = Button(background_normal="./images/wrong.png", on_press=self.next_card)
        button_layout.add_widget(cross_btn)

        check_btn = Button(background_normal="./images/right.png", on_press=self.known_cards)
        button_layout.add_widget(check_btn)

        root.add_widget(button_layout)

        Clock.schedule_once(self.next_card, 0)  # Schedule the first card update

        return root

    def next_card(self, *args):
        if self.current_card:
            self.ids.box.remove_widget(self.current_card)

        self.current_card = random.choice(self.learn_dict)
        french_word = self.current_card["French"]
        self.card_word.text = french_word
        self.card_title.text = "French"
        self.card_background.source = "./images/card_front.png"

        if self.flip_timer:
            Clock.unschedule(self.flip_timer)

        self.flip_timer = Clock.schedule_once(self.flip_card, 3)

    def known_cards(self, *args):
        self.learn_dict.remove(self.current_card)
        data1 = pandas.DataFrame(self.learn_dict)
        data1.to_csv("./data/words_to_learn.csv", index=False)
        self.next_card()

    def flip_card(self, *args):
        english_word = self.current_card["English"]
        self.card_title.text = "English"
        self.card_word.text = english_word
        self.card_background.source = "./images/card_back.png"


if __name__ == '__main__':
    FlashyApp().run()
