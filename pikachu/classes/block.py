#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = zjp
# Date: 2019/9/6


import os
import cocos
import random


class Block(cocos.sprite.Sprite):
    # 生成地图上的随机块状物
    def __init__(self, position):
        super(Block, self).__init__('black.png')

        # 锚点
        self.image_anchor = 0, 0
        x, y = position
        if x == 0:
            self.scale_x = 4.5
            self.scale_y = 1
        else:
            self.scale_x = 0.5 + random.random() * 1.5
            self.scale_y = min(max(y - 50 + random.random() * 100, 50), 300) / 100
            self.position = x + 50 + random.random() * 100, 0
