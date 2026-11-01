import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Headless environment setup for GitHub Actions
os.environ["QT_QPA_PLATFORM"] = "offscreen"

WIDTH, HEIGHT = 1920, 1080
FPS = 30 
DURATION_SEC = 22
TOTAL_FRAMES = FPS * DURATION_SEC

output_video_path = "sdf_dryfood_ad.mp4"

# Safe video codec for cloud servers
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_path, fourcc, FPS, (WIDTH, HEIGHT))

print("Rendering high-contrast video frames...")

# GitHub সার্ভারে ডিফল্ট ফন্ট ছোট হলে কাজ করার জন্য ফন্ট স্কেলিং ফাংশন
def draw_scaled_text(draw, text, position, size, fill, anchor="mm"):
    try:
        # লিনাক্স সার্ভারের স্ট্যান্ডার্ড বড় ফন্ট ট্রাই করা হচ্ছে
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except IOError:
        font = ImageFont.load_default()
    
    # ফন্ট লোড ডিফল্ট হলে টেক্সটকে বড় করে ড্র করার ট্রিক
    draw.text(position, text, fill=fill, font=font, anchor=anchor)

# Pre-create background to save memory
base_bg = Image.new("RGBA", (WIDTH, HEIGHT), (253, 251, 247, 255))

for frame_idx in range(TOTAL_FRAMES):
    time_sec = frame_idx / FPS
    frame_img = base_bg.copy()
    draw = ImageDraw.Draw(frame_img)
    
    # Scene 1: 0.00 - 3.00s (Intro)
    if 0.0 <= time_sec < 3.0:
        opacity = int((time_sec / 3.0) * 255)
        draw_scaled_text(draw, "SDF Private Limited", (WIDTH//2, HEIGHT//2 - 120), 90, (74, 38, 18, opacity))
        draw_scaled_text(draw, "Healthy Eating, Everyday Living", (WIDTH//2, HEIGHT//2 + 40), 55, (212, 175, 55, opacity))
        
    # Scene 2 & 3: 3.00 - 12.00s (Dry Foods Offer)
    elif 3.0 <= time_sec < 12.0:
        draw_scaled_text(draw, "PREMIUM QUALITY DRY FOODS", (WIDTH//2, HEIGHT//2 - 300), 85, (74, 38, 18, 255))
        
        scale = min(1.0, (time_sec - 3.0) * 2)
        banner_w, banner_h = int(1100 * scale), int(220 * scale)
        if banner_w > 0 and banner_h > 0:
            box_pos = [(WIDTH//2 - banner_w//2, HEIGHT//2 - banner_h//2), (WIDTH//2 + banner_w//2, HEIGHT//2 + banner_h//2)]
            draw.rounded_rectangle(box_pos, radius=25, fill=(212, 175, 55, 255))
            if scale == 1.0:
                draw_scaled_text(draw, "FESTIVE OFFER: 30% OFF!", (WIDTH//2, HEIGHT//2), 80, (255, 255, 255, 255))
                
        # Floating dry food particles animation
        for i in range(6):
            angle = (time_sec * 2) + (i * (np.pi / 3))
            cx = int(WIDTH//2 + 500 * np.cos(angle))
            cy = int(HEIGHT//2 + 350 + 60 * np.sin(angle * 2))
            draw.ellipse([cx-55, cy-55, cx+55, cy+55], fill=(160, 82, 45, 255))
            
    # Scene 4: 12.00 - 16.50s (Freshness Pack)
    elif 12.0 <= time_sec < 16.50:
        draw_scaled_text(draw, "Freshness & Purity Guaranteed", (WIDTH//2, HEIGHT//2 - 250), 80, (34, 139, 34, 255))
        draw.rectangle([WIDTH//2 - 200, HEIGHT//2 - 50, WIDTH//2 + 200, HEIGHT//2 + 300], fill=(230, 230, 230, 255), outline=(74, 38, 18), width=8)
        draw_scaled_text(draw, "SDF FRESH PACK", (WIDTH//2, HEIGHT//2 + 120), 50, (74, 38, 18, 255))

    # Scene 5 & 6: 16.50 - 22.00s (Outro & Logo)
    else:
        draw_scaled_text(draw, "SDF PRIVATE LIMITED", (WIDTH//2, HEIGHT//2 - 180), 95, (74, 38, 18, 255))
        draw_scaled_text(draw, '"Goodness in every bite."', (WIDTH//2, HEIGHT//2 - 40), 60, (212, 175, 55, 255))
        
        button_pos = [(WIDTH//2 - 450, HEIGHT//2 + 120), (WIDTH//2 + 450, HEIGHT//2 + 220)]
        draw.rounded_rectangle(button_pos, radius=15, fill=(74, 38, 18, 255))
        draw_scaled_text(draw, "ORDER NOW: ://sdfprivate.com", (WIDTH//2, HEIGHT//2 + 170), 50, (255, 255, 255, 255))
        
    frame_bgr = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGBA2BGR)
    video_writer.write(frame_bgr)

video_writer.release()
print(f"Render completed successfully! Output: {output_video_path}")
