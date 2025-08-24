from PIL import Image, ImageDraw, ImageFont
import random
from .concepts import get_semantic_shift_data
from .explain import analyze_semantic_shift_with_ai

def get_system_font():
    """Get system available font"""
    try:
        # Try system font
        return ImageFont.truetype("arial.ttf", 16)
    except:
        try:
            # Alternative font
            return ImageFont.truetype("simhei.ttf", 16)
        except:
            # Use default font
            return ImageFont.load_default()

def generate_semantic_shift_image(word: str, file_path: str, use_ai: bool = True) -> str:
    """Generate semantic shift line chart for philosophical concepts and save as PNG.
    
    Args:
        word: Philosophical concept word
        file_path: Path to save the image
        use_ai: Whether to use AI-generated data
        
    Returns:
        Saved image path
    """
    width, height = 1000, 700  # 增加尺寸以容纳更多信息
    margin = 80

    # Use English labels
    eras = ["Ancient Greece", "Medieval", "Modern", "Contemporary"]
    
    # Get concept semantic shift data
    if use_ai:
        # 尝试使用AI生成数据
        ai_data = analyze_semantic_shift_with_ai(word)
        if ai_data.get("ai_generated") and "error" not in ai_data:
            shift_data = ai_data
            print(f"使用AI生成的数据: {word}")
        else:
            print(f"AI生成失败，使用预设数据: {word}")
            shift_data = get_semantic_shift_data(word)
    else:
        shift_data = get_semantic_shift_data(word)
    
    if "values" in shift_data and len(shift_data["values"]) == 4:
        values = shift_data["values"]
    else:
        # If no predefined data, generate reasonable random data
        random.seed(hash(word) % 1000)  # Ensure same word generates same data
        values = [random.uniform(0.2, 0.8) for _ in range(4)]
        values.sort()  # Sort to make curve more reasonable

    img = Image.new("RGB", (width, height), (248, 249, 250))
    draw = ImageDraw.Draw(img)
    
    # Get font
    font = get_system_font()
    title_font = get_system_font()  # 可以调整大小
    small_font = get_system_font()  # 可以调整大小

    # Draw grid
    for i in range(1, 5):
        x = margin + (width - 2 * margin) * i / 4
        draw.line((x, margin, x, height - margin - 100), fill=(220, 220, 220), width=1)
    
    for i in range(1, 6):
        y = height - margin - 100 - (height - 2 * margin - 100) * i / 5
        draw.line((margin, y, width - margin, y), fill=(220, 220, 220), width=1)

    # Coordinate axes
    draw.line((margin, height - margin - 100, width - margin, height - margin - 100), fill=(0, 0, 0), width=3)
    draw.line((margin, margin, margin, height - margin - 100), fill=(0, 0, 0), width=3)

    # Calculate coordinate points
    xs, ys = [], []
    for i, v in enumerate(values):
        x = margin + (width - 2 * margin) * i / (len(values) - 1)
        y = height - margin - 100 - (height - 2 * margin - 100) * v
        xs.append(x)
        ys.append(y)

    # Draw line
    for i in range(len(values) - 1):
        draw.line((xs[i], ys[i], xs[i + 1], ys[i + 1]), fill=(33, 150, 243), width=4)
    
    # Draw nodes
    for i in range(len(values)):
        # Outer circle
        draw.ellipse((xs[i] - 8, ys[i] - 8, xs[i] + 8, ys[i] + 8), fill=(255, 255, 255), outline=(33, 150, 243), width=2)
        # Inner circle
        draw.ellipse((xs[i] - 4, ys[i] - 4, xs[i] + 4, ys[i] + 4), fill=(33, 150, 243))

    # Era labels
    for i, era in enumerate(eras):
        x = xs[i]
        y = height - margin - 80
        # Use font to draw text
        bbox = draw.textbbox((0, 0), era, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width//2, y), era, fill=(0, 0, 0), font=font)

    # Y-axis labels
    for i, t in enumerate([0.0, 0.2, 0.4, 0.6, 0.8, 1.0]):
        y = height - margin - 100 - (height - 2 * margin - 100) * t
        draw.line((margin - 5, y, margin, y), fill=(0, 0, 0), width=2)
        label = f"{t:.1f}"
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((margin - 70, y - 10), label, fill=(0, 0, 0), font=font)

    # Title
    title = f"AI-Generated Semantic Shift Analysis: {word}"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    draw.text((width//2 - title_width//2, 30), title, fill=(0, 0, 0), font=title_font)
    
    # Subtitle
    subtitle = "Semantic Complexity / Abstraction Level Changes"
    bbox = draw.textbbox((0, 0), subtitle, font=font)
    subtitle_width = bbox[2] - bbox[0]
    draw.text((width//2 - subtitle_width//2, 60), subtitle, fill=(100, 100, 100), font=font)

    # Add value labels
    for i, (x, y, v) in enumerate(zip(xs, ys, values)):
        label = f"{v:.2f}"
        draw.text((x + 15, y - 20), label, fill=(33, 150, 243), font=font)

    # Add AI-generated insights if available
    if shift_data.get("ai_generated") and "overall_trend" in shift_data:
        # Overall trend
        trend_text = f"Overall Trend: {shift_data['overall_trend']}"
        if len(trend_text) > 80:
            trend_text = trend_text[:77] + "..."
        draw.text((margin, height - 60), trend_text, fill=(50, 50, 50), font=font)
        
        # Key insights
        if "key_insights" in shift_data and len(shift_data["key_insights"]) > 0:
            insights_text = f"Key Insights: {', '.join(shift_data['key_insights'][:2])}"
            if len(insights_text) > 80:
                insights_text = insights_text[:77] + "..."
            draw.text((margin, height - 40), insights_text, fill=(50, 50, 50), font=font)
        
        # Data source indicator
        draw.text((width - margin - 150, height - 40), "AI-Generated Data", fill=(76, 175, 80), font=font)
    else:
        # Use preset data description if available
        if "description" in shift_data:
            description = shift_data["description"]
            # Simple handling of long descriptions
            if len(description) > 80:
                description = description[:77] + "..."
            draw.text((margin, height - 60), f"Note: {description}", fill=(100, 100, 100), font=font)
        
        # Data source indicator
        draw.text((width - margin - 150, height - 40), "Preset Data", fill=(158, 158, 158), font=font)

    img.save(file_path, "PNG")
    return file_path



