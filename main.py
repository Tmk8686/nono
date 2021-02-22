from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleViewfrom kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
 
class PongPaddle(Widget):
    score = NumericProperty(0) ## очки игрока
 
    ## Отскок мячика при коллизии с панелькой игрока
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
 
            ball.velocity = vel.x, vel.y + offset
 
 
class PongBall(Widget):
 
    # Скорость движения нашего шарика по двум осям
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
 
    # Создаем условный вектор
    velocity = ReferenceListProperty(velocity_x, velocity_y)
 
    # Заставим шарик двигаться
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
 
class PongGame(Widget):
    ball = ObjectProperty(None) # это будет наша связь с объектом шарика
    player1 = ObjectProperty(None) # Игрок 1
    player2 = ObjectProperty(None) # Игрок 2
 
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(0, 360))
 
    def update(self, dt):
        self.ball.move() # двигаем шарик в каждом обновлении экрана
 
        # проверка отскока шарика от панелек игроков
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
 
        # отскок шарика по оси Y
        if(self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1 # инверсируем текущую скорость по оси Y
 
        # отскок шарика по оси X
        # тут если шарик смог уйти за панельку игрока, то есть игрок не успел отбить шарик
        # то это значит что он проиграл и мы добавим +1 очко противнику
        if self.ball.x < self.x:
            # Первый игрок проиграл, добавляем 1 очко второму игроку
            self.player2.score += 1
            self.serve_ball(vel=(4,0)) # заново спавним шарик в центре
 
        if self.ball.x > self.width:
            # Второй игрок проиграл, добавляем 1 очко первому игроку
            self.player1.score += 1
            self.serve_ball(vel=(-4,0)) # заново спавним шарик в центре
 
    # Событие прикосновения к экрану
    def on_touch_move(self, touch):
        # первый игрок может касаться только своей части экрана (левой)
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
 
        # второй игрок может касаться только своей части экрана (правой)
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
 
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60) # 60 FPS
        return game
 
if __name__ == '__main__':
    PongApp().run()
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
from datetime import datetime
import os
import ast
import time


class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')
        box.add_widget(Button(text='Дневник питания', on_press=lambda x:
                              set_screen('list_food')))
        box.add_widget(Button(text='Добавить блюдо в дневник питания',
                              on_press=lambda x: set_screen('add_food')))
        self.add_widget(box)


class SortedListFood(Screen):
    def __init__(self, **kw):
        super(SortedListFood, self).__init__(**kw)

    def on_enter(self):  # Будет вызвана в момент открытия экрана

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        back_button = Button(text='< Назад в главное меню',
                             on_press=lambda x: set_screen('menu'),
                             size_hint_y=None, height=dp(40))
        self.layout.add_widget(back_button)
        root = RecycleView(size_hint=(1, None), size=(Window.width,
                                                      Window.height))
        root.add_widget(self.layout)
        self.add_widget(root)

        dic_foods = ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

        for f, d in sorted(dic_foods.items(), key=lambda x: x[1]):
            fd = f.decode('u8') + ' ' + (datetime.fromtimestamp(d).strftime('%Y-%m-%d'))
            btn = Button(text=fd, size_hint_y=None, height=dp(40))
            self.layout.add_widget(btn)

    def on_leave(self):  # Будет вызвана в момент закрытия экрана

        self.layout.clear_widgets()  # очищаем список


class AddFood(Screen):

    def buttonClicked(self, btn1):
        if not self.txt1.text:
            return
        self.app = App.get_running_app()
        self.app.user_data = ast.literal_eval(
            self.app.config.get('General', 'user_data'))
        self.app.user_data[self.txt1.text.encode('u8')] = int(time.time())

        self.app.config.set('General', 'user_data', self.app.user_data)
        self.app.config.write()

        text = "Последнее добавленное блюдо:  " + self.txt1.text
        self.result.text = text
        self.txt1.text = ''

    def __init__(self, **kw):
        super(AddFood, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')
        back_button = Button(text='< Назад в главное меню', on_press=lambda x:
                             set_screen('menu'), size_hint_y=None, height=dp(40))
        box.add_widget(back_button)
        self.txt1 = TextInput(text='', multiline=False, height=dp(40),
                              size_hint_y=None, hint_text="Название блюда")
        box.add_widget(self.txt1)
        btn1 = Button(text="Добавить блюдо", size_hint_y=None, height=dp(40))
        btn1.bind(on_press=self.buttonClicked)
        box.add_widget(btn1)
        self.result = Label(text='')
        box.add_widget(self.result)
        self.add_widget(box)


def set_screen(name_screen):
    sm.current = name_screen


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SortedListFood(name='list_food'))
sm.add_widget(AddFood(name='add_food'))


class FoodOptionsApp(App):
    def __init__(self, **kvargs):
        super(FoodOptionsApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, '%(appname)s.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(FoodOptionsApp, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        return sm


if __name__ == '__main__':
    FoodOptionsApp().run()
