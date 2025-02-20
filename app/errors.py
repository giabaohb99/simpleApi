from fastapi import HTTPException
from pydantic import BaseModel

# Định nghĩa cấu trúc cho phản hồi lỗi
class ErrorResponse(BaseModel):
    code: int
    message: str

# Hàm tiện ích để tạo HTTPException với cấu trúc lỗi chuẩn
def raise_custom_http_exception(status_code: int, message: str):
    error_response = ErrorResponse(code=status_code, message=message).dict()
    raise HTTPException(status_code=status_code, detail=error_response)