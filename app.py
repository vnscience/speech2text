import streamlit as st
import whisper
import os
import tempfile

# Cấu hình trang web
st.set_page_config(page_title="AI Audio Transcriber", page_icon="🎙️")

st.title("🎙️ Chuyển đổi Âm thanh thành Văn bản")
st.markdown("Hệ thống sử dụng công nghệ **OpenAI Whisper** để nhận diện giọng nói.")

# --- SIDEBAR: Cấu hình ---
st.sidebar.header("Cấu hình Model")
model_size = st.sidebar.selectbox(
    "Chọn kích thước mô hình (Càng lớn càng chính xác nhưng chậm hơn):",
    ["tiny", "base", "small", "medium", "large"],
    index=1  # Mặc định là 'base'
)

@st.cache_resource
def load_model(size):
    return whisper.load_model(size)

# Tải model vào bộ nhớ
with st.spinner(f"Đang tải mô hình {model_size}..."):
    model = load_model(model_size)

# --- CHÍNH: Upload và Xử lý ---
uploaded_file = st.file_uploader("Tải lên file âm thanh", type=["mp3", "wav", "m4a", "flac", "ogg"])

if uploaded_file is not None:
    # Hiển thị trình phát nhạc để người dùng nghe lại
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Bắt đầu chuyển đổi"):
        with st.spinner("Đang nhận diện giọng nói..."):
            try:
                # Tạo file tạm thời để Whisper có thể đọc
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                # Thực hiện transcribe
                result = model.transcribe(tmp_path)
                text = result["text"]

                # Hiển thị kết quả
                st.subheader("Kết quả văn bản:")
                st.text_area("Văn bản trích xuất:", value=text, height=300)

                # Nút tải file text về máy
                st.download_button(
                    label="Tải văn bản về máy (.txt)",
                    data=text,
                    file_name=f"{uploaded_file.name}.txt",
                    mime="text/plain"
                )

                # Xóa file tạm sau khi xử lý
                os.remove(tmp_path)
                
            except Exception as e:
                st.error(f"Lỗi: {e}")

st.divider()
st.caption("Lưu ý: Thời gian xử lý phụ thuộc vào độ dài file và cấu hình máy tính của bạn.")