from PIL import Image, ImageDraw, ImageFont

def create_logo(text):
    # Set the image size and background color
    img_size = (300, 200)
    bg_color = (255, 0, 0)  # Red background (adjust as needed)

    # Create a blank image with the specified background color
    img = Image.new("RGB", img_size, bg_color)
    draw = ImageDraw.Draw(img)

    # Choose a font and size
    font = ImageFont.load_default()

    # Calculate text size and position
    text_size = draw.textsize(text, font)
    text_position = ((img.width - text_size[0]) // 2, (img.height - text_size[1]) // 2)

    # Draw the text on the image
    draw.text(text_position, text, font=font, fill=(255, 255, 255))  # White text

    # Save the image
    img.save("logo.png")

# Example usage:
create_logo("Your Logo Text")
