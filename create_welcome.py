from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), 'data', 'welcome.png')


def create_welcome_image():
    width, height = 800, 400
    img = Image.new('RGB', (width, height), '#1a1a2e')
    draw = ImageDraw.Draw(img)

    for i in range(height):
        r = int(26 + (102 - 26) * i / height)
        g = int(26 + (45 - 26) * i / height)
        b = int(46 + (140 - 46) * i / height)
        draw.rectangle([0, i, width, i], fill=(r, g, b))

    draw.rectangle([50, 30, width - 50, height - 30], outline='#e94560', width=3)
    draw.rectangle([55, 35, width - 55, height - 35], outline='#0f3460', width=1)

    title = "🎉 بوت التحميل الشامل 🎉"
    subtitle = "Download from All Platforms"
    platforms = "📥 TikTok    📸 Instagram    🎬 YouTube    🐦 Twitter    📘 Facebook"
    footer = f"أرسل الرابط وسأقوم بالباقي!"

    try:
        font_large = ImageFont.truetype("arial.ttf", 40)
        font_medium = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 18)
        font_footer = ImageFont.truetype("arial.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large
        font_footer = font_large

    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 65), title, fill='#e94560', font=font_large)

    bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 125), subtitle, fill='#e0e0e0', font=font_medium)

    draw.line([(100, 160), (width - 100, 160)], fill='#e94560', width=1)

    bbox = draw.textbbox((0, 0), platforms, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 195), platforms, fill='#a0a0c0', font=font_small)

    bbox = draw.textbbox((0, 0), footer, font=font_footer)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 300), footer, fill='#e94560', font=font_footer)

    draw.line([(200, 340), (width - 200, 340)], fill='#0f3460', width=1)
    powered = "@z0taw"
    bbox = draw.textbbox((0, 0), powered, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 355), powered, fill='#e0e0e0', font=font_small)

    img.save(FONT_PATH, 'PNG')
    return FONT_PATH


if __name__ == '__main__':
    path = create_welcome_image()
    print(f"Welcome image created: {path}")
