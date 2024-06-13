# Library
from ursina import *
from random import randint

# Font 
FONT = "gui_assets/ARCADE_N.TTF"

# Halaman Homepage
class HomePage(Entity):
    def __init__(self):
        super().__init__()

        print("Initializing Home Page")
        self.main_menu = Entity(
            parent=self,
            enabled=True
        )

        Entity(
            model="quad",
            parent=self.main_menu,
            position=(0, 0, 1),
            scale=(2560/167.7, 1440/167.7),
            texture='gui_assets/background.png'
        )
        Entity(
            parent=self.main_menu,
            model="quad",
            texture="gui_assets/logo.png",
            position=(0, 1, 0),
            scale=(2560/167.7, 1440/167.7)
        )
        self.start_button = Button(
            text="TAP TO PLAY",
            color=color.rgba(53/255, 243/255, 64/255, 0.8),
            scale=(7, 1),
            y=-1.5,
            parent=self.main_menu,
            radius=0.35,
            highlight_color=color.rgba(1, 0, 0, 0.8)
        )
        self.start_button.text_entity.font = FONT
        self.start_button.text_entity.color = color.rgb(13/255, 107/255, 148/255)
        self.start_button.on_click = self.play_game

    def play_game(self):
        print("Start Game button clicked")
        self.main_menu.enabled = False
        gameplay.start_game()

# Halaman Gameplay
class GamePlay(Entity):
    def __init__(self):
        super().__init__()
        print("Initializing Game Play")

        self.keranjang = Entity(
            model="quad",
            texture="gameplay_assets/keranjang.png",
            scale=(1.5, 1),
            position=(0, -3.5),
            collider='box',
            enabled=False  
        )

        self.background = Entity(
            model="quad",
            texture="gameplay_assets/game.png",
            scale=(2560/167.7, 1440/167.7),
            z=1
        )

        self.score = 0
        self.game_over = False
        self.score_text = Text(text=f'Score: {self.score}', position=(-0.85, 0.45), scale=2)
        self.game_over_text = Text(
            text='Game Over! Press R to Restart',
            position=(0, 0),
            scale=2,
            enabled=False,
            origin=(0, 0.5),  
            background=True,  
            background_color=color.black66,  
            color=color.red  
        )

        self.exit_button = Button(
            text="Exit",
            color=color.rgba(255, 0, 0, 0.8),
            scale=(2.5, 0.7),  
            x=-6,  
            y=-3.5,  
            parent=self,
            radius=0.35,
            highlight_color=color.rgba(1, 0, 0, 0.8),
            on_click=self.exit_game
        )
        self.exit_button.text_entity.font = FONT
        self.exit_button.text_entity.color = color.rgb(255, 255, 255)

        self.fruits = []
        self.bombs = []

        self.enabled = False

    def update(self):
        if not self.game_over and self.enabled:
            self.keranjang.x += held_keys['d'] * time.dt * 5
            self.keranjang.x -= held_keys['a'] * time.dt * 5

            for fruit in self.fruits[:]:
                fruit.y -= time.dt * 5
                if fruit.intersects(self.keranjang).hit:
                    destroy(fruit)
                    self.fruits.remove(fruit)
                    self.score += 1
                elif fruit.y < -4:
                    destroy(fruit)
                    self.fruits.remove(fruit)

            for bomb in self.bombs[:]:
                bomb.y -= time.dt * 5
                if bomb.intersects(self.keranjang).hit:
                    self.game_over = True
                    self.game_over_text.enabled = True
                    self.stop_spawning()
                elif bomb.y < -4:
                    destroy(bomb)
                    self.bombs.remove(bomb)

            self.score_text.text = f'Score: {self.score}'
        elif self.game_over and held_keys['r']:
            self.restart_game()

    def spawn_fruit(self):
        fruit = Entity(
            model="quad",
            texture="gameplay_assets/strawberry.png",
            scale=(1, 1),
            position=(randint(-7, 7), 4),
            collider='box'
        )
        self.fruits.append(fruit)

    def spawn_mango(self):
        mango = Entity(
            model="quad",
            texture="gameplay_assets/mangga.png",
            scale=(1, 1),
            position=(randint(-7, 7), 4),
            collider='box'
        )
        self.fruits.append(mango)

    def spawn_banana(self):
        banana = Entity(
            model="quad",
            texture="gameplay_assets/banana.png",
            scale=(1, 1),
            position=(randint(-7, 7), 4),
            collider='box'
        )
        self.fruits.append(banana)

    def spawn_pear(self):
        pear = Entity(
            model="quad",
            texture="gameplay_assets/pir.png",
            scale=(1, 1),
            position=(randint(-7, 7), 4),
            collider='box'
        )
        self.fruits.append(pear)

    def spawn_bomb(self):
        bomb = Entity(
            model="quad",
            texture="gameplay_assets/ulet.png",
            scale=(1, 1),
            position=(randint(-7, 7), 4),
            collider='box'
        )
        self.bombs.append(bomb)

    def start_game(self):
        self.enabled = True
        self.game_over = False
        self.score = 0
        self.score_text.text = f'Score: {self.score}'
        self.game_over_text.enabled = False
        self.keranjang.enabled = True  
        self.start_spawning()

    def restart_game(self):
        self.score = 0
        self.game_over = False
        self.game_over_text.enabled = False
        for fruit in self.fruits:
            destroy(fruit)
        for bomb in self.bombs:
            destroy(bomb)
        self.fruits.clear()
        self.bombs.clear()
        self.score_text.text = f'Score: {self.score}'
        self.keranjang.enabled = True  
        self.start_spawning()

    def start_spawning(self):
        self.fruit_sequence = Sequence(Func(self.spawn_fruit), Wait(1), loop=True)
        self.fruit_sequence.start()
        
        self.mango_sequence = Sequence(Func(self.spawn_mango), Wait(2), loop=True)  
        self.mango_sequence.start()

        self.banana_sequence = Sequence(Func(self.spawn_banana), Wait(4), loop=True)  
        self.banana_sequence.start()

        self.pear_sequence = Sequence(Func(self.spawn_pear), Wait(3), loop=True) 
        self.pear_sequence.start()
        
        self.bomb_sequence = Sequence(Func(self.spawn_bomb), Wait(2), loop=True)
        self.bomb_sequence.start()

    def stop_spawning(self):
        self.fruit_sequence.pause()
        self.mango_sequence.pause()
        self.banana_sequence.pause()
        self.pear_sequence.pause()
        self.bomb_sequence.pause()

    def exit_game(self):
        exit()

app = Ursina()

home_page = HomePage()
gameplay = GamePlay()

app.run()