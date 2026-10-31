import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ১. হেডলেস এনভায়রনমেন্ট সেটআপ (Cloud Render-এর জন্য জরুরি)
# সার্ভারে যাতে ডিসপ্লে ইরর না আসে তার জন্য এটি সেট করা হলো
os.environ["QT_QPA_PLATFORM"] = "offscreen"

WIDTH, HEIGHT = 1920, 1080
FPS = 60
DURATION_SEC = 22
TOTAL_FRAMES = FPS * DURATION_SEC

# আউটপুট ফাইল প্যাথ (ক্লাউড স্টোরেজে সেভ করার জন্য প্রস্তুত)
output_video_path = "sdf_dryfood_ad.mp4"

# ক্লাউড সার্ভারের জন্য সবচেয়ে নিরাপদ ভিডিও কোডেক (avc1 / mp4v)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_path, fourcc, FPS, (WIDTH, HEIGHT))

print("Cloud host rendering started for SDF Private Limited...")

# ২. ক্লাউড সার্ভারে ফন্টের সমস্যা এড়ানোর জন্য লজিক
# সার্ভারে সাধারণত উইন্ডোজের মতো সরাসরি 'arial.ttf' থাকে না, তাই ডিফল্ট ফন্ট লোড ব্যাকআপ রাখা হয়েছে
def get_font(size):
    try:
        # লিনাক্স/ক্লাউড সার্ভারের কমন ফন্ট প্যাথ চেকিং
        linux_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if os.path.exists(linux_font_path):
            return ImageFont.truetype(linux_font_path, size)
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

font_large = get_font(80)
font_sub = get_font(50)
font_bold = get_font(95)

# ৩. ফ্রেম বাই ফ্রেম রেন্ডারিং লুপ
for frame_idx in range(TOTAL_FRAMES):
    time_sec = frame_idx / FPS
    
    # ব্যাকগ্রাউন্ড তৈরি (Premium Warm Light Pastel)
    frame_img = Image.new("RGBA", (WIDTH, HEIGHT), (253, 251, 247, 255))
    draw = ImageDraw.Draw(frame_img)
    
    # সিন ১: ০.০০ - ৩.০০ সেকেন্ড
    if 0.0 <= time_sec < 3.0:
        opacity = int((time_sec / 3.0) * 255)
        draw.text((WIDTH//2, HEIGHT//2 - 100), "SDF Private Limited", fill=(74, 38, 18, opacity), font=font_large, anchor="mm")
        draw.text((WIDTH//2, HEIGHT//2 + 20), "Healthy Eating, Everyday Living", fill=(212, 175, 55, opacity), font=font_sub, anchor="mm")
        
    # সিন ২ ও ৩: ৩.০০ - ১২.০০ সেকেন্ড
    elif 3.0 <= time_sec < 12.0:
        draw.text((WIDTH//2, HEIGHT//2 - 250), "PREMIUM QUALITY DRY FOODS", fill=(74, 38, 18, 255), font=font_large, anchor="mm")
        
        scale = min(1.0, (time_sec - 3.0) * 2)
        banner_w, banner_h = int(900 * scale), int(180 * scale)
        if banner_w > 0 and banner_h > 0:
            box_pos = [(WIDTH//2 - banner_w//2, HEIGHT//2 - banner_h//2), (WIDTH//2 + banner_w//2, HEIGHT//2 + banner_h//2)]
            draw.rounded_rectangle(box_pos, radius=20, fill=(212, 175, 55, 255))
            
            if scale == 1.0:
                draw.text((WIDTH//2, HEIGHT//2), "FESTIVE OFFER: 30% OFF!", fill=(255, 255, 255, 255), font=font_bold, anchor="mm")
                
        # ড্রাই ফ্রুটস অ্যানিমেশন
        for i in range(6):
            angle = (time_sec * 2) + (i * (np.pi / 3))
            cx = int(WIDTH//2 + 400 * np.cos(angle))
            cy = int(HEIGHT//2 + 300 + 50 * np.sin(angle * 2))
            draw.ellipse([cx-40, cy-40, cx+40, cy+40], fill=(160, 82, 45, 255))
            
    # সিন ৪: ১২.০০ - ১৬.৫০ সেকেন্ড
    elif 12.0 <= time_sec < 16.50:
        draw.text((WIDTH//2, HEIGHT//2 - 200), "Freshness & Purity Guaranteed", fill=(34, 139, 34, 255), font=font_large, anchor="mm")
        draw.rectangle([WIDTH//2 - 150, HEIGHT//2 - 50, WIDTH//2 + 150, HEIGHT//2 + 250], fill=(220, 220, 220, 255), outline=(74, 38, 18), width=5)
        draw.text((WIDTH//2, HEIGHT//2 + 100), "SDF FRESH PACK", fill=(74, 38, 18, 255), font=font_sub, anchor="mm")

    # সিন ৫ ও ৬: ১৬.৫০ - ২২.০০ সেকেন্ড (End Card)
    else:
        draw.text((WIDTH//2, HEIGHT//2 - 150), "SDF PRIVATE LIMITED", fill=(74, 38, 18, 255), font=font_bold, anchor="mm")
        draw.text((WIDTH//2, HEIGHT//2 - 30), '"Goodness in every bite."', fill=(212, 175, 55, 255), font=font_sub, anchor="mm")
        
        # কল টু অ্যাকশন বাটন
        button_pos = [(WIDTH//2 - 350, HEIGHT//2 + 100), (WIDTH//2 + 350, HEIGHT//2 + 180)]
        draw.rounded_rectangle(button_pos, radius=10, fill=(74, 38, 18, 255))
        draw.text((WIDTH//2, HEIGHT//2 + 140), "ORDER NOW: ://sdfprivate.com", fill=(255, 255, 255, 255), font=font_sub, anchor="mm")
        
    # ইমেজ ফ্রেমকে ভিডিওর জন্য কনভার্ট করা
    frame_bgr = cv2.cvtColor(np.array(frame_img), cv2.COLOR_RGBA2BGR)
    video_writer.write(frame_bgr)

video_writer.release()
print(f"Render successfully completed! 
