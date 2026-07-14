import os
import chardet
from typing import Optional, Tuple


class EncodingDetector:
    ENCODINGS = [
        'utf-8-sig',
        'utf-8',
        'utf-16-le',
        'utf-16-be',
        'windows-1256',
        'cp1252',
        'cp1250',
        'iso-8859-1',
    ]
    
    @classmethod
    def detect(cls, file_path: str) -> str:
        if not os.path.exists(file_path):
            return 'utf-8'
            
        for encoding in cls.ENCODINGS:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                    return encoding
            except:
                continue
                
        try:
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read(10000))
                if result and result['encoding']:
                    return result['encoding']
        except:
            pass
            
        return 'utf-8'


class FileConverter:
    @classmethod
    def convert_file(
        cls,
        source_path: str,
        target_path: str,
        source_enc: str = "تشخیص خودکار",
        target_enc: str = "UTF-8"
    ) -> Tuple[bool, Optional[str]]:
        try:
            if not os.path.exists(source_path):
                return False, "فایل وجود ندارد"
                
            enc_map = {
                "UTF-8 with BOM": "utf-8-sig",
                "UTF-8": "utf-8",
                "UTF-16 LE": "utf-16-le",
                "UTF-16 BE": "utf-16-be",
                "Windows-1256": "windows-1256",
                "ANSI": "windows-1256",
                "Unicode": "utf-16-le",
            }
                
            actual_enc = source_enc
            if source_enc == "تشخیص خودکار" or "خودکار" in source_enc:
                actual_enc = EncodingDetector.detect(source_path)
            else:
                actual_enc = enc_map.get(source_enc, "utf-8")
            
            target_enc_real = enc_map.get(target_enc, "utf-8")
            
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            content = None
            try:
                with open(source_path, 'r', encoding=actual_enc) as f:
                    content = f.read()
            except UnicodeDecodeError:
                for enc in ['utf-8', 'cp1252', 'windows-1256', 'utf-16-le']:
                    if enc != actual_enc:
                        try:
                            with open(source_path, 'r', encoding=enc) as f:
                                content = f.read()
                                break
                        except:
                            continue
                if content is None:
                    return False, "خطا در خواندن فایل"
            
            target_path = cls._unique_name(target_path)
            
            with open(target_path, 'w', encoding=target_enc_real, errors='ignore') as f:
                f.write(content)
                
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    @classmethod
    def _unique_name(cls, file_path: str) -> str:
        if not os.path.exists(file_path):
            return file_path
            
        directory = os.path.dirname(file_path)
        name, ext = os.path.splitext(os.path.basename(file_path))
        
        counter = 1
        while True:
            new_name = f"{name}_{counter}{ext}"
            new_path = os.path.join(directory, new_name)
            if not os.path.exists(new_path):
                return new_path
            counter += 1