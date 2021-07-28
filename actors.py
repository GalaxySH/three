from cocos.sprite import Sprite
from cocos.euclid import Vector2
from cocos.collision_model import CircleShape, AARectShape
from cocos.actions import IntervalAction, Delay, CallFunc, MoveBy
from pyglet.image import ImageGrid, Animation, load
import math
from cocos.text import Label

raw = load("assets/explosion.png")
seq = ImageGrid(raw, 1, 8)  # one row eight columns
explosion_img = Animation.from_image_sequence(seq, 0.07, False)  # no loop


class Actor(Sprite):
    def __init__(self, image, x, y):
        super().__init__(image)

        pos = Vector2(x, y)
        self.position = pos
        self._cshape = CircleShape(pos, self.width * 0.5)

    @property
    def cshape(self):
        self._cshape.center = Vector2(self.x, self.y)
        return self._cshape


class Hit(IntervalAction):
    def __init__(self, duration=0.5):
        self.duration = duration

    def update(self, pct_elapsed):
        self.target.color = (255, 255 * pct_elapsed, 255 * pct_elapsed)


class Explosion(Sprite):
    def __init__(self, pos):
        super().__init__(explosion_img, pos)
        self.do(Delay(0.7) * CallFunc(self.kill))


class Enemy(Actor):
    def __init__(self, x, y, actions, game):
        super().__init__('tank.png', x, y)

        self.game = game
        self.max_health = 100
        self.health = 100
        self.points = 20
        self.destroyed_by_player = False  # points if True

        self.health_bar = TankHealthLabel(self.max_health / 20, 1)
        self.health_bar.position = (self.x, self.y - 20)
        self.game.add(self.health_bar)

        self.schedule(self.manage_bar)
        self.do(actions)  # move, turn, move, whatever

    def explode(self):
        self.parent.add(Explosion(self.position))
        self.kill()

    def manage_bar(self, _):
        rotation = self.rotation
        self.health_bar.position = (self.x, self.y - 20)

    def hit(self):
        self.health -= 25
        self.do(Hit())

        # self.health_bar.element.text = ''.join(['▋' for _ in range(round(self.health / 20))])
        self.health_bar.set_percent(self.health / self.max_health)

        if self.health <= 0 and self.is_running:
            self.destroyed_by_player = True
            self.explode()


class TankHealthLabel(Label):
    def __init__(self, bars, prc):
        super().__init__('', font_size=5, anchor_x='center',
                         anchor_y='top', color=(255, 80, 0, 255))

        self.percent = prc
        self.bars = bars

        self.set_percent(self.percent)

    def set_percent(self, prc: float):
        bars_display = ''.join(['▋' for _ in range(round(self.bars * prc))])
        self.element.text = bars_display


class HealthBar(Sprite):
    def __init__(self, pos):
        super().__init__('assets/health_bar.png', pos)

        self.percent = 1.0

    def set_percent(self, prc: float):
        self.percent = 1.0
