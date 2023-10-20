import streamlit as st
from PIL import Image
import io

def compress_and_convert_to_jpg(img, quality=85):
    """
    이미지를 압축하고 JPG로 변환하여 바이트로 반환합니다.
    """
    buffered = io.BytesIO()
    img.convert('RGB').save(buffered, format="JPEG", quality=quality)
    return buffered.getvalue()

st.title('Image Compressor & JPG Converter')

uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpeg', 'jpg', 'bmp', 'tiff'])

if uploaded_file:
    original_size = len(uploaded_file.read())
    st.write(f"Original Image Size: {original_size / 1024:.2f} KB")
    
    # 파일 포인터를 다시 처음으로 되돌리기 위함
    uploaded_file.seek(0)
    img = Image.open(uploaded_file)
    
    quality = st.slider('Select JPG Quality', 10, 100, 85)
    compressed_img_data = compress_and_convert_to_jpg(img, quality)
    compressed_size = len(compressed_img_data)
    
    # 컬럼으로 이미지를 나누기
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img, caption="Uploaded Image.", use_column_width=True)
        st.write(f"Original Image Size: {original_size / 1024:.2f} KB")
        
    with col2:
        st.image(compressed_img_data, caption="Compressed Image.", use_column_width=True)
        st.write(f"Compressed Image Size: {compressed_size / 1024:.2f} KB")
    
    st.download_button("Download Compressed JPG", compressed_img_data, "compressed.jpg", "image/jpeg")

    # 로드 시간 예상치 계산 (예: 5MB/s 속도로 다운로드할 경우)
    download_speed = 5 * 1024 * 1024  # 5 MB/s in bytes
    estimated_time_compressed = compressed_size / download_speed
    st.write(f"Estimated load time for compressed image (at 5MB/s): {estimated_time_compressed:.2f} seconds")

