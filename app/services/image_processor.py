# app/services/image_processor.py
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from typing import Tuple
import os

class ImageProcessor:
    def __init__(self):
        # フォントファイルのパスを設定
        font_path = os.path.join(os.path.dirname(__file__), '../../assets/fonts/Arial.ttf')
        self.font = ImageFont.truetype(font_path, 60)

    async def add_lgtm_text(self, image_url: str, text: str = "LGTM") -> BytesIO:
        """画像にLGTMテキストを追加する"""
        # 画像をダウンロード
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # 画像のサイズを取得
        width, height = image.size

        # 必要に応じてリサイズ（最大幅1200px）
        if width > 1200:
            ratio = 1200.0 / width
            width = 1200
            height = int(height * ratio)
            image = image.resize((width, height), Image.Resampling.LANCZOS)

        # 描画オブジェクトを作成
        draw = ImageDraw.Draw(image)

        # テキストのサイズを取得
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # テキストの位置を計算（中央配置）
        x = (width - text_width) / 2
        y = (height - text_height) / 2

        # テキストを描画（縁取り付き）
        outline_color = 'black'
        text_color = 'white'
        outline_width = 3

        # 縁取りを描画
        for adj in range(-outline_width, outline_width + 1):
            for adj2 in range(-outline_width, outline_width + 1):
                draw.text((x + adj, y + adj2), text, font=self.font, fill=outline_color)

        # メインのテキストを描画
        draw.text((x, y), text, font=self.font, fill=text_color)

        # 画像をBytesIOオブジェクトに保存
        output = BytesIO()
        image.save(output, format='PNG')
        output.seek(0)

        return output

image_processor = ImageProcessor()