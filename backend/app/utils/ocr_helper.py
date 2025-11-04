import pytesseract
from PIL import Image
import re

def extract_marks_from_image(image_path):
    try:
        image = Image.open(image_path)
        
        text = pytesseract.image_to_string(image)
        
        lines = text.split('\n')
        
        extracted_marks = []
        
        for line in lines:
            numbers = re.findall(r'\d+', line)
            if len(numbers) >= 2:
                try:
                    obtained = int(numbers[0])
                    total = int(numbers[1])
                    
                    if 0 <= obtained <= total <= 100:
                        extracted_marks.append({
                            'marks_obtained': obtained,
                            'total_marks': total,
                            'percentage': round((obtained / total) * 100, 2),
                            'raw_text': line.strip()
                        })
                except ValueError:
                    continue
        
        return {
            'extracted_text': text,
            'marks': extracted_marks[:5],
            'count': len(extracted_marks)
        }
    
    except Exception as e:
        raise Exception(f'OCR extraction failed: {str(e)}')
