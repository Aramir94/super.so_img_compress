import streamlit as st
from PIL import Image, ImageSequence
import io

def compress_and_convert_to_jpg(img, quality=85):
    """
    이미지를 압축하고 JPG로 변환하여 바이트로 반환합니다.
    """
    buffered = io.BytesIO()
    img.convert('RGB').save(buffered, format="JPEG", quality=quality)
    return buffered.getvalue()

def compress_gif(img, quality=85, frame_skip=2):
    """
    GIF 이미지의 각 프레임 퀄리티를 줄이고 프레임 수를 줄입니다.
    """
    frames = [frame.copy() for index, frame in enumerate(ImageSequence.Iterator(img)) if index % frame_skip == 0]
    buffered = io.BytesIO()
    frames[0].save(buffered, format="GIF", append_images=frames[1:], save_all=True, quality=quality, loop=0)
    return buffered.getvalue()

st.title('Image & GIF Compressor')

# 선택 모드 (이미지 또는 GIF)
mode = st.sidebar.selectbox("Choose mode", ["Image", "GIF"])

if mode == "Image":
    file_type = ['png', 'jpeg', 'jpg', 'bmp', 'tiff']
    processing_function = compress_and_convert_to_jpg
    download_format = "image/jpeg"
    download_name = "compressed.jpg"
else:  # mode == "GIF":
    file_type = ['gif']
    processing_function = compress_gif
    download_format = "image/gif"
    download_name = "compressed.gif"
    frame_skip = st.sidebar.slider('Select frame skip', 1, 5, 2)
    st.sidebar.text('Every nth frame will be kept.')

uploaded_file = st.sidebar.file_uploader("Choose a file...", type=file_type)
quality = st.sidebar.slider('Select Quality', 10, 100, 85)

if uploaded_file:
    original_size = len(uploaded_file.read())
    uploaded_file.seek(0)
    img = Image.open(uploaded_file)
    
    if mode == "GIF":
        compressed_img_data = processing_function(img, quality, frame_skip)
    else:
        compressed_img_data = processing_function(img, quality)
    
    compressed_size = len(compressed_img_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img, caption="Uploaded Image/GIF.", width=300)
        st.write(f"Original Size: {original_size / 1024:.2f} KB")
        
    with col2:
        st.image(compressed_img_data, caption="Compressed Image/GIF.", width=300)
        st.write(f"Compressed Size: {compressed_size / 1024:.2f} KB")
    
    st.sidebar.download_button(f"Download Compressed {mode}", compressed_img_data, download_name, download_format)

    download_speed = 5 * 1024 * 1024  # 5 MB/s in bytes
    estimated_time_original = original_size / download_speed
    estimated_time_compressed = compressed_size / download_speed
    
    st.write(f"Estimated load time (at 5MB/s):")
    st.write(f"Original {mode}: {estimated_time_original:.2f} seconds")
    st.write(f"Compressed {mode}: {estimated_time_compressed:.2f} seconds")

