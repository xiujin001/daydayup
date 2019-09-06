#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = zjp
# Date: 2019/9/5
import string
import random
from PIL import Image, ImageDraw, ImageFont


# pillow是PIL（Python成像库）的一个分支，它不再被维护。所以，为了保持向后兼容性，
# 往往使用旧的模块名称——PIL。所以，我们直接import PIL就可以了。

class Captcha:
    '''
    :param captcha_size:图片验证码的尺寸
    :param font_size:验证字体的大小
    :param text_number:验证码的字符数
    :param line_number:干扰线条数量
    :param background_color:图片背景色
    :param sources:取样字符集
    :param save_format:图片保存格式
    :return:
    '''

    def __init__(self, captcha_size=(150, 80),
                 font_size=40, text_number=4,
                 line_number=6, background_color=(255, 255, 255),
                 sources=None, save_format='png'):

        self.captcha_size = captcha_size
        self.font_size = font_size
        self.text_number = text_number
        self.line_number = line_number
        self.background_color = background_color
        self.format = save_format
        if sources:
            self.sources = sources
        else:
            self.sources = string.ascii_letters + string.digits

    def get_text(self):
        # 从sources字符集里面根据验证码数量随机生成一串字符
        text = random.sample(self.sources, k=self.text_number)
        return ''.join(text)

    def get_font_color(self):
        # 随机获取验证码中的字符的RGB颜色
        font_color = (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))
        return font_color

    def get_line_color(self):
        line_color = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))
        return line_color

    def draw_text(self, draw, text, font, captcha_width, captcha_height, spacing=20):
        '''
        在图片上绘制传入的字符
        :param draw: 生成的画笔对象
        :param text: 绘制的字符
        :param font: 采用的字体
        :param captcha_width:验证码宽度
        :param captcha_height: 验证码高度
        :param spacing: 字符之间间隔
        :return:
        '''
        # 获得字符串的宽度,高度
        text_width, text_height = font.getsize(text)
        # 每个字符的大概宽度
        every_value_width = int(text_width / 4)

        # 这一串字符的总长度
        text_length = len(text)
        # 每两个字符之间拥有间隙,获取总的间隙???
        total_spacing = (text_length - 1) * spacing

        if total_spacing + text_width >= captcha_width:
            raise ValueError('字体加中间空隙超过图片总宽度')

        # 获取第一个字符绘制位置
        start_width = int(captcha_width - text_width - total_spacing)
        start_height = int((captcha_height - text_height) / 2)

        # 依次绘制每个字符
        for value in text:
            position = start_width, start_height
            print(position)
            # 绘制text
            draw.text(position, value, font=font, fill=self.get_font_color())
            # 改变下一个字符的起始绘制
            start_width = start_width + every_value_width + spacing

    def draw_line(self, draw, captcha_width, captcha_height):
        '''
        绘制线条
        :param draw:画笔对象
        :param captcha_width:验证码宽度
        :param captcha_height: 验证码高度
        :return:
        '''
        # 随即获取开始位置的坐标
        begin = (random.randint(0, captcha_width / 2), random.randint(0, captcha_height / 2))
        # 随机获取结束位置的坐标
        end = (random.randint(captcha_width / 2, captcha_width), random.randint(captcha_height / 2, captcha_height))
        draw.line([begin, end], fill=self.get_line_color())

    def draw_point(self, draw, point_chance, width, height):
        '''
        绘制干扰圆点
        :param draw: 画笔对象
        :param point_chance:绘制圆点的概率,point_chance / 100
        :param width: 验证码宽度
        :param height: 验证码高度
        :return:
        '''

        # 按照概率随机绘制小圆点
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp < point_chance:
                    draw.point((w, h), fill=self.get_line_color())

    def make_captcha(self):
        # 制作验证码
        # 获取验证码的宽度,高度
        width, height = self.captcha_size
        # 生成一张图片
        captcha = Image.new('RGB', self.captcha_size, self.background_color)
        # 获取字体对象
        font = ImageFont.truetype('simkai.ttf', self.font_size)
        # 获取画笔对象
        draw = ImageDraw.Draw(captcha)
        # 得到绘制的字符
        text = self.get_text()

        # 绘制字符
        self.draw_text(draw, text, font, width, height)

        # 绘制线条
        for i in range(self.line_number):
            self.draw_line(draw, width, height)

        # 绘制小圆点 10/100=10%的概率
        self.draw_point(draw, 10, width, height)

        # 保存图片
        captcha.save('captcha', format=self.format)
        # 显示图片
        captcha.show()


if __name__ == '__main__':
    a = Captcha()
    a.make_captcha()
