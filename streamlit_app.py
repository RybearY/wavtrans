import streamlit as st
from pydub import AudioSegment
import os
from pathlib import Path
import tempfile

st.title("WAV 파일 재인코딩 도구")
st.write("WAV 파일을 FLAC으로 변환한 후 다시 WAV로 변환하여 파일 무결성 문제를 해결합니다.")

uploaded_file = st.file_uploader("WAV 파일을 업로드하세요", type=['wav'])

if uploaded_file is not None:
    # 업로드된 파일 표시
    st.audio(uploaded_file, format="audio/wav")
    
    # 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    
    # 원본 WAV 파일 저장
    original_wav_path = os.path.join(temp_dir, "original.wav")
    with open(original_wav_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    # FLAC으로 변환
    flac_path = os.path.join(temp_dir, "converted.flac")
    st.text("FLAC으로 변환 중...")
    sound = AudioSegment.from_wav(original_wav_path)
    sound.export(flac_path, format="flac")
    
    # 다시 WAV로 변환
    new_wav_path = os.path.join(temp_dir, "reencoded.wav")
    st.text("WAV로 재변환 중...")
    flac_sound = AudioSegment.from_file(flac_path, format="flac")
    flac_sound.export(new_wav_path, format="wav")
    
    # 변환된 파일 표시
    st.subheader("재인코딩된 WAV 파일")
    with open(new_wav_path, 'rb') as f:
        st.audio(f.read(), format="audio/wav")
    
    # 다운로드 버튼
    with open(new_wav_path, 'rb') as f:
        st.download_button(
            label="재인코딩된 WAV 파일 다운로드",
            data=f.read(),
            file_name="reencoded.wav",
            mime="audio/wav"
        )
