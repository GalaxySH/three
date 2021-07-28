import random

from cocos.scene import Scene
from cocos.layer import Layer
from cocos.director import director
from cocos.collision_model import  CollisionManagerGrid
from cocos.scenes import FadeTransition, SplitColsTransition
from cocos.text import Label

import actors
from scenario import get_scenario_1, get_scenario_2, Scenario


def new_game():
    scenario = get_scenario_1()
    background = scenario.get_background()
    hud = None
    game_layer = GameLayer(hud, scenario)
    return Scene(background, game_layer)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self, hud, scenario: Scenario):
        super().__init__()

        self.hud = hud
        self.scenario = scenario

        self.schedule(self.game_loop)

    def create_enemy(self):
        spawn_x, spawn_y = self.scenario.enemy_start
        x = spawn_x + random.uniform(-10, 10)
        y = spawn_y + random.uniform(-10, 10)
        self.add(actors.Enemy(x, y, self.scenario.enemy_actions, self))

    def game_loop(self, _):
        spawn_chance = 0.005
        if random.random() < spawn_chance:
            self.create_enemy()
