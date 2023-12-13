import os
import random
from PIL import Image, ImageDraw, ImageFont
from telethon import events

# Function to generate a random background color
def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

# Function to create a logo with random text on a random background
async def create_random_logo(event, text):
    # Generate a random background color
    bg_color = random_color()

    # Create a blank image with the random background color
    img_size = (300, 200)
    img = Image.new("RGB", img_size, bg_color)
    draw = ImageDraw.Draw(img)

    # Choose a random font and size
    font = ImageFont.load_default()

    # Calculate text size and position
    text_size = font.getsize(text)
    text_position = ((img.width - text_size[0]) // 2, (img.height - text_size[1]) // 2)

    # Draw the text on the image
    draw.text(text_position, text, font=font, fill=(255, 255, 255))  # White text

    # Save the image
    img_path = "random_logo.png"
    img.save(img_path)

    # Send the image as a file
    await event.client.send_file(
        event.chat_id,
        img_path,
        caption=f"Random Logo: {text}",
        force_document=True,
        reply_to=event.message.id,
    )

    # Cleanup: Remove the temporary image file
    os.remove(img_path)

# Event handler for the .logo command
@events.register(events.NewMessage(pattern=r"^.logo (.+)", outgoing=True))
async def logo_command_handler(event):
    # Extract the text from the command
    text = event.pattern_match.group(1)

    # Generate a random text if not provided
    if not text:
        text = "Lorem Ipsum"  # Replace with your preferred default text

    # Create the random logo
    await create_random_logo(event, text)

# Add a help command for the .logo command
@events.register(events.NewMessage(pattern=r"^.help logo", outgoing=True))
async def help_command_handler(event):
    await event.respond(".logo <text> - Create a logo with the specified text (or random text).")
