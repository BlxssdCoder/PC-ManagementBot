import mouse
from PIL import Image, ImageDraw, ImageGrab


async def get_screenshot():
    currentMouseX, currentMouseY = mouse.get_position()
    img = ImageGrab.grab()
    img.save("screen.png", "png")
    img = Image.open("screen.png")
    draw = ImageDraw.Draw(img)
    draw.polygon((currentMouseX, currentMouseY, currentMouseX, currentMouseY +
                 20, currentMouseX + 13, currentMouseY + 13), fill="white", outline="black")
    img.save("screen_with_mouse.png", "PNG")
