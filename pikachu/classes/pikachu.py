#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = zjp
# Date: 2019/9/6
import cocos
import os


class Pikachu(cocos.sprite.Sprite):
    # 实现一个皮卡丘类来生成皮卡实例
    def __init__(self):
        super(Pikachu, self).__init__('pikachu.png')
        # 是否可以跳跃
        self.jumpable = False
        # 行进速度
        self.speed = 0
        # 锚点
        self.image_anchor = 0, 0
        # 皮卡丘的位置
        self.position = 80, 280
        self.schedule(self.update)

    def jump(self, h):
        # 声控跳跃
        if self.jumpable:
            self.y += 1
            self.speed -= max(min(h, 10), 7)
            self.jumpable = False

    def land(self, y):
        # 着陆后静止
        if self.y > y - 25:
            self.jumpable = True
            self.speed = 0
            self.y = y

    def update(self, dt):
        # 更新(重力下降)
        self.speed += 10 * dt
        self.y -= self.speed
        if self.y < -85:
            self.reset()

    def reset(self):
        self.parent.reset()
        self.jumpable = False
        self.speed = 0
        self.position = 80, 280
