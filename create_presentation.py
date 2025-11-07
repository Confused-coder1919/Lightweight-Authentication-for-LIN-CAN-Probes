from PIL import Image, ImageDraw, ImageFont

def create_summary_slide():
    img = Image.new('RGB',(1600,900),'white'); d = ImageDraw.Draw(img)
    try:
        title = ImageFont.truetype("Arial.ttf", 60)
        big = ImageFont.truetype("Arial.ttf", 40); small = ImageFont.truetype("Arial.ttf", 26)
    except:
        title = big = small = ImageFont.load_default()
    d.text((800,80),"PROJECT SUMMARY", font=title, fill="black", anchor="mm")
    rows = [
        ("PERFORMANCE","0.048 ms","< 10 ms req"),
        ("SECURITY","100%","replay & spoofing blocked"),
        ("THROUGHPUT","481k msg/s","measured average"),
        ("TESTS","27/27","all passed"),
    ]
    y = 220
    for name,val,desc in rows:
        d.text((400,y), name, font=small, fill="black", anchor="mm")
        d.text((800,y), val,  font=big,   fill="black", anchor="mm")
        d.text((1200,y),desc, font=small, fill="gray",  anchor="mm")
        y += 140
    d.text((800,850),"Lightweight Automotive MAC | Hackathon 2025", font=small, fill="gray", anchor="mm")
    img.save("summary_slide.png"); print("✅ Saved: summary_slide.png")

if __name__ == "__main__":
    create_summary_slide()
