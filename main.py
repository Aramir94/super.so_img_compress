import streamlit as st
from PIL import Image, ImageSequence
import io
import base64

def compress_and_convert_to_jpg(img, quality=85):
    buffered = io.BytesIO()
    img.convert('RGB').save(buffered, format="JPEG", quality=quality)
    return buffered.getvalue()

def compress_gif(img, quality=85, frame_interval=100):
    frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
    buffered = io.BytesIO()
    frames[0].save(buffered, format="GIF", append_images=frames[1:], save_all=True, quality=quality, loop=0, duration=frame_interval)
    return buffered.getvalue()

def image_to_base64(img_data):
    img_str = base64.b64encode(img_data).decode()
    return f"data:image/gif;base64,{img_str}"

st.title('Image & GIF Compressor')

mode = st.sidebar.selectbox("Choose mode", ["Image", "GIF"])

if mode == "Image":
    file_type = ['png', 'jpeg', 'jpg', 'bmp', 'tiff']
    processing_function = compress_and_convert_to_jpg
    download_format = "image/jpeg"
    download_name = "compressed.jpg"
else:
    file_type = ['gif']
    processing_function = compress_gif
    download_format = "image/gif"
    download_name = "compressed.gif"

uploaded_file = st.sidebar.file_uploader("Choose a file...", type=file_type)
quality = st.sidebar.slider('Select Quality', 10, 100, 85)

if uploaded_file:
    original_size = len(uploaded_file.read())
    uploaded_file.seek(0)
    img = Image.open(uploaded_file)

    if mode == "GIF":
        frame_interval = st.sidebar.slider('Frame Interval (ms)', 10, 500, 100)
        compressed_img_data = processing_function(img, quality, frame_interval)
    else:
        compressed_img_data = processing_function(img, quality)

    compressed_size = len(compressed_img_data)
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Uploaded {mode}:")
        if mode == "Image":
            st.image(uploaded_file.getvalue(), width=300)
        else:
            st.markdown(f'<img src="{image_to_base64(uploaded_file.getvalue())}" width="300">', unsafe_allow_html=True)
        st.write(f"Original Size: {original_size / 1024:.2f} KB")

    with col2:
        st.write(f"Compressed {mode}:")
        if mode == "Image":
            st.image(compressed_img_data, width=300)
        else:
            st.markdown(f'<img src="{image_to_base64(compressed_img_data)}" width="300">', unsafe_allow_html=True)
        st.write(f"Compressed Size: {compressed_size / 1024:.2f} KB")

    st.sidebar.download_button(f"Download Compressed {mode}", compressed_img_data, download_name, download_format)

    download_speed = 5 * 1024 * 1024
    estimated_time_original = original_size / download_speed
    estimated_time_compressed = compressed_size / download_speed

    st.write(f"Estimated load time (at 5MB/s):")
    st.write(f"Original {mode}: {estimated_time_original:.2f} seconds")
    st.write(f"Compressed {mode}: {estimated_time_compressed:.2f} seconds")
