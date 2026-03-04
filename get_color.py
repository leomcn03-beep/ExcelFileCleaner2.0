from PIL import Image
import collections

def get_dominant_color(image_path):
    img = Image.open(image_path)
    img = img.resize((150, 150))  # Resize for speed
    result = img.convert('P', palette=Image.ADAPTIVE, colors=1)  # Reduce to 1 color
    result = result.convert('RGB')
    main_color = result.getpixel((0, 0))
    return '#{:02x}{:02x}{:02x}'.format(main_color[0], main_color[1], main_color[2])

if __name__ == "__main__":
    image_path = r"C:/Users/Leo McNicholas/.gemini/antigravity/brain/6eab9864-7197-49f8-8438-fb504f52d550/uploaded_media_1769429936109.png"
    try:
        hex_color = get_dominant_color(image_path)
        print(f"DOMINANT_COLOR:{hex_color}")
    except Exception as e:
        print(f"Error: {e}")
