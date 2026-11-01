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

print("Rendering video frames efficiently...")

# Default system fonts for GitHub Linux runner
font_large = ImageFont.load_default()
font_sub = ImageFont.load_default()
font_bold = ImageFont.load_default()

# Pre-create background to save memory
base_bg = Image.new("RGBA", (WIDTH, HEIGHT), (253, 251, 247, 255))

for frame_idx in range(TOTAL_FRAMES):
    time_sec = frame_idx / FPS
    frame_img = base_bg.copy()
    draw = ImageDraw.Draw(frame_img)
    
    # Scene 1: 0.00 - 3.00s (Intro)
    if 0.0 <= time_sec < 3.0:
        opacity = int((time_sec / 3.0) * 255)
        draw.text((WIDTH//2, HEIGHT//2 - 100), "SDF Private Limited", fill=(74, 38, 18, opacity), font=font_large, anchor="mm")
        draw.text((WIDTH//2, HEIGHT//2 + 20), "Healthy Eating, Everyday Living", fill=(212, 175, 55, opacity), font=font_sub, anchor="mm")
        
    # Scene 2 & 3: 3.00 - 12.00s (Dry Foods Offer)
    elif 3.0 <= time_sec < 12.0:
        draw.text((WIDTH//2, HEIGHT//2 - 250), "PREMIUM QUALITY DRY FOODS", fill=(74, 38, 18, 255), font=font_large, anchor="mm")
        
        scale = min(1.0, (time_sec - 3.0) * 2)
        banner_w, banner_h = int(900 * scale), int(180 * scale)
        if banner_w > 0 and banner_h > 0:
            box_pos = [(WIDTH//2 - banner_w//2, HEIGHT//2 - banner_h//2), (WIDTH//2 + banner_w//2, HEIGHT//2 + banner_h//2)]
            draw.rounded_rectangle(box_pos, radius=20, fill=(212, 175, 55, 255))
            if scale == 1.0:
                draw.text((WIDTH//2, HEIGHT//2), "FESTIVE OFFER: 30% OFF!", fill=(255, 255, 255, 255), font=font_bold, anchor="mm")
                
        # Floating dry food particles animation
        for i in range(6):
            angle = (time_sec * 2) + (i * (np.pi / 3))
            cx = int(WIDTH//2 + 400 * np.cos(angle))
            cy = int(HEIGHT//2 + 300 + 50 * np.sin(angle * 2))
            draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(160, 82, 45, 255))
            
    # Scene 4: 12.00 - 16.50s (Freshness Pack)
    elif 12.0 <= time_sec < 16.50:
        draw.text((WIDTH//2, HEIGHT//2 - 200), "Freshness & Purity Guaranteed", fill=(34, 139, 34, 255), font=font_large, anchor="mm")
        draw.rectangle([WIDTH//2 - 150, HEIGHT//2 - 50, WIDTH//2 + 150, HEIGHT//2 + 250], fill=(220, 220, 220, 255), outline=(74, 38, 18), width=5)
        draw.text((WIDTH//2, HEIGHT//2 + 100), "SDF FRESH PACK", fill=(74, 38, 18, 255), font=font_sub, anchor="mm")

    # Scene 5 & 6: 16.50 - 22.00s (Outro & Logo)
    else:
        draw.text((WIDTH//2, HEIGHT//2 - 150), "SDF PRIVATE LIMITED", fill=(74, 38, 18, 255), font=font_bold, anchor="mm")
        draw.text((WIDTH//2, HEIGHT//2 - 30), '"Goodness in every bite."', fill=(212, 175, 55, 255), font=font_sub, anchor="mm")
        
        button_pos = [(WIDTH//2 - 350, HEIGHT//2 + 100), (WIDTH//2 + 350, HEIGHT//2 + 180)]
        draw.rounded_rectangle(button_pos, radius=10, fill=(74, 38, 18, 255))
        draw.text((WIDTH//2, HEIGHT//2 + 140), "ORDER NOW: ://sdfprivate.com", fill=(255, 255, 255, 255), font=font_sub, anchor="mm")
        
    frame_bgr = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGBA2BGR)
    video_writer.write(frame_bgr)

video_writer.release()
print(f"Render completed successfully! Output: {output_video_path}")
