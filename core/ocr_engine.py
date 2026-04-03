import sys
import json
import os
import platform

def extract_text_from_image(image_path):
    current_os = platform.system()
    
    # 策略 1: Mac 原生引擎 (ocrmac)
    if current_os == "Darwin":
        try:
            from ocrmac import ocrmac
            print(f"[Engine] Using Mac Native (ocrmac)")
            annotations = ocrmac.OCR(image_path).recognize()
            return "\n".join([text for text, confidence, bbox in annotations])
        except ImportError:
            print("[Warning] ocrmac not found, falling back...")

    # 策略 2: 通用引擎 (EasyOCR) - 適合無 Tesseract 二進位檔的環境
    try:
        import easyocr
        print(f"[Engine] Using EasyOCR (Cross-platform)")
        reader = easyocr.Reader(['en', 'ch_tra']) # 支援英、繁中
        result = reader.readtext(image_path, detail=0)
        return "\n".join(result)
    except ImportError:
        print("[Warning] easyocr not found, falling back...")

    # 策略 3: 傳統引擎 (PyTesseract) - 需要系統安裝 Tesseract-OCR
    try:
        import pytesseract
        from PIL import Image
        print(f"[Engine] Using PyTesseract")
        return pytesseract.image_to_string(Image.open(image_path), lang='chi_tra+eng')
    except ImportError:
        return "[Error] No OCR engine available. Please install 'easyocr' or 'pytesseract'."
    except Exception as e:
        return f"[Error] OCR failed: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ocr_engine.py [path_to_image]")
    else:
        img_path = sys.argv[1]
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
        else:
            text_result = extract_text_from_image(img_path)
            print("--- OCR RAW START ---")
            print(text_result)
            print("--- OCR RAW END ---")
