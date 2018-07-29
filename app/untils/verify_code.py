"""
随机生成验证码模块
AUTH:TTC
DATE:2018-06-16 15:33:52
VERSION: 0.0.1
"""
from random import choice, randint

from PIL import Image, ImageDraw, ImageFont, ImageFilter


class VerifyCode(object):
    """生成验证码模块"""

    def __init__(self, length=4, width=160, height=50, font_size=40):
        """
        验证码初始化方法
        :param length: 验证码长度 默认length=4
        :param width: 验证码图片宽度 默认width=160
        :param height: 验证码图片高度 默认height=50
        :param font_size: 字体大小 默认font_size=40
        """
        self._random_code = ''  # 验证码字符串
        self._verify_code_image = None  # PIL图片Image对象
        self._length = length  # 验证码长度
        self._width = width  # 图片宽度
        self._height = height  # 图片高度
        self._font_size = font_size  # 字体大小
        self.set_random_code()  # 初始化验证码字符
        self.set_image()  # 绘制图片

    def set_random_code(self):
        """
        随机生成验证码的方法
        将生成的验证码赋值给self._random_code属性
        :return: None
        """
        lib = '1234567890qwertyuiopasdfghjklzxcvbnm'  # 验证码字符库
        code = ''  # 生成的验证码
        for _ in range(self._length):  # 循环随机取一个字符
            code += choice(lib)
        self._random_code = code  # 赋值给当前对象的random_code属性

    @staticmethod
    def random_color(s=0, e=255):
        """
        随机生成RGB颜色
        :param s: 开始范围
        :param e: 结束范围
        :return: Tuple (r, g, b)
        """
        s = s if 0 <= s <= 255 else 0  # 限定范围 0 - 255
        e = e if 0 <= e <= 255 else 255  # 限定范围 0 - 255
        s, e = (s, e) if s < e else (e, s)  # 限定大小 s 必须小于 e
        return randint(s, e), randint(s, e), randint(s, e)

    def set_image(self):
        """
        生成验证码图片
        :return: None
        """
        # 创建一个Image对象, 全白的画布
        image = Image.new('RGB', (self._width, self._height), (255, 255, 255))
        # 创建一个字体对象
        font = ImageFont.truetype('arial.ttf', self._font_size)
        # 创建一个画图对象
        draw = ImageDraw.Draw(image)
        # for循环随机生成噪点
        for x in range(self._width):
            for y in range(self._height):
                temp = x + y + randint(0, 10)
                if temp % 10 == 0:
                    draw.point((x, y), fill=self.random_color(0, 255))
        # for循环将字符添加到图中
        for t in range(self._length):
            dev_x = randint(15, 20)  # 随机左右浮动
            dev_y = randint(0, 5)  # 随机上下浮动
            x, y = ((self._width/4) * t)-5 + dev_x, dev_y
            # 将字符通过随机颜色画到图片中
            draw.text((x, y), self._random_code[t],
                      font=font, fill=self.random_color(0, 200))
        # 进行高斯模糊
        image = image.filter(ImageFilter.GaussianBlur)
        # 将图片对象赋值给当前对象的verify_code_image属性
        draw.line((0,20,100,20),fill=(0,0,0),width=5)
        self._verify_code_image = image

    @property
    def verify_code(self):
        """
        获取当前对象的验证码字符串
        :return:
        """
        return self._random_code

    @property
    def verify_image(self):
        """
        获取当前验证码的图片对象
        :return:
        """
        return self._verify_code_image

    def get_verify(self):
        """
        通过元组返回验证码字符串和图片对象
        :return: 验证码字符,PIL image对象图片
        """
        return self._random_code, self._verify_code_image