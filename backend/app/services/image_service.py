import io
import base64
from typing import Tuple, Optional
from PIL import Image, ImageOps, ImageEnhance

class ImageService:
    @staticmethod
    def validate_image(file_bytes: bytes) -> Tuple[bool, str]:
        """Kiểm tra định dạng và tính hợp lệ của ảnh (FR-02, FR-03)"""
        max_size_mb = 15
        if len(file_bytes) > max_size_mb * 1024 * 1024:
            return False, f"Dung lượng ảnh vượt quá giới hạn {max_size_mb}MB."
        try:
            with Image.open(io.BytesIO(file_bytes)) as img:
                img.verify()
                format_name = img.format.lower() if img.format else ""
                if format_name not in ["jpeg", "jpg", "png", "webp"]:
                    return False, f"Định dạng '{format_name}' không được hỗ trợ. Vui lòng tải file JPG, PNG."
            return True, "Hợp lệ"
        except Exception as e:
            return False, f"Tệp ảnh bị lỗi hoặc không thể đọc: {str(e)}"

    @staticmethod
    def preprocess_image(
        file_bytes: bytes,
        rotate_angle: int = 0,
        enhance_contrast: bool = True,
        max_dimension: int = 2048
    ) -> Tuple[bytes, str]:
        """Tiền xử lý ảnh: xoay, tăng độ tương phản, chuẩn hóa kích thước (FR-04)"""
        with Image.open(io.BytesIO(file_bytes)) as img:
            # Xử lý EXIF Orientation tự động
            img = ImageOps.exif_transpose(img)
            
            # Xoay theo góc người dùng yêu cầu
            if rotate_angle in [90, 180, 270]:
                img = img.rotate(-rotate_angle, expand=True)

            # Chuyển về RGB nếu cần
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Tăng độ tương phản nhẹ nếu ảnh mờ/tối
            if enhance_contrast:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.2)

            # Resize nếu kích thước quá lớn để tối ưu truyền tải
            if max(img.size) > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

            output = io.BytesIO()
            img.save(output, format="JPEG", quality=90)
            processed_bytes = output.getvalue()
            b64_str = base64.b64encode(processed_bytes).decode("utf-8")
            return processed_bytes, b64_str

image_service = ImageService()
