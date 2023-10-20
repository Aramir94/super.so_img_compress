import streamlit as st
from PIL import Image, ImageSequence
import io
import base64

def get_image_with_href(data, file_name="image", file_type="jpeg"):
    encoded = base64.b64encode(data).decode()
    href = f'<a href="data:image/{file_type};base64,{encoded}" download="{file_name}.{file_type}"><img src="data:image/{file_type};base64,{encoded}" width=300/></a>'
    return href

def compress_and_convert_to_jpg(img, quality=85):
    buffered = io.BytesIO()
    img.convert('RGB').save(buffered, format="JPEG", quality=quality)
    return buffered.getvalue()

def compress_gif(img, quality=85, skip_frames=1, frame_interval=100):
    frames = [frame.copy() for index, frame in enumerate(ImageSequence.Iterator(img)) if index % skip_frames == 0]
    buffered = io.BytesIO()
    frames[0].save(buffered, format="GIF", append_images=frames[1:], save_all=True, quality=quality, loop=0, duration=frame_interval)
    return buffered.getvalue()

st.title('Image & GIF Compressor')

mode = st.sidebar.selectbox("Choose mode", ["Image", "GIF"])

uploaded_file = st.sidebar.file_uploader("Choose a file...", type=['png', 'jpeg', 'jpg', 'bmp', 'tiff', 'gif'])

if mode == "Image":
    quality = st.sidebar.slider('Select JPG Quality', 10, 100, 85)
    processing_function = compress_and_convert_to_jpg
    download_format = "jpeg"
    download_name = "compressed"
else:
    quality = st.sidebar.slider('Select GIF Quality', 10, 100, 85)
    skip_frames = st.sidebar.slider('Skip frames (e.g. 2 means every second frame will be used)', 1, 5, 1)
    frame_interval = st.sidebar.slider('Frame Interval (ms)', 10, 500, 100)
    processing_function = lambda img: compress_gif(img, quality, skip_frames, frame_interval)
    download_format = "gif"
    download_name = "compressed"

if uploaded_file:
    original_size = len(uploaded_file.read())
    uploaded_file.seek(0)
    img = Image.open(uploaded_file)

    compressed_img_data = processing_function(img)
    compressed_size = len(compressed_img_data)

    col1, col2 = st.columns(2)

    with col1:
        if mode == "Image":
            st.image(uploaded_file, caption="Original", width=300)
        else:
            st.markdown(get_image_with_href(uploaded_file.getvalue(), "original", "gif"), unsafe_allow_html=True)
        st.write(f"Original Size: {original_size / 1024:.2f} KB")

    with col2:
        st.markdown(get_image_with_href(compressed_img_data, download_name, download_format), unsafe_allow_html=True)
        st.write(f"Compressed Size: {compressed_size / 1024:.2f} KB")

    download_speed = 5 * 1024 * 1024  # 5 MB/s in bytes
    estimated_time_original = original_size / download_speed
    estimated_time_compressed = compressed_size / download_speed

    st.write(f"Estimated load time (at 5MB/s):")
    st.write(f"Original {mode}: {estimated_time_original:.2f} seconds")
    st.write(f"Compressed {mode}: {estimated_time_compressed:.2f} seconds")
