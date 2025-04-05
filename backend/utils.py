import numpy as np
import matplotlib.pyplot as plt
import librosa
import os
from scipy.signal import spectrogram

# 限制图像尺寸
MAX_LENGTH = 50000

# 生成经典波形风格
def generate_waveform(y, output_path):
    plt.figure(figsize=(6, 6))
    y = y[:MAX_LENGTH]  # 限制数据长度
    plt.plot(y, color="black")
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

# 生成极简主义波形风格
def generate_minimal_waveform(y, output_path):
    plt.figure(figsize=(6, 6))
    y = y[:MAX_LENGTH]  # 限制数据长度
    plt.plot(y[::100], color="black")  # 简化波形
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

# 生成频谱几何风格
def generate_spectral_waveform(y, sr, output_path):
    f, t, Sxx = spectrogram(y, fs=sr)
    plt.figure(figsize=(6, 6))
    plt.imshow(np.log(Sxx), cmap='hot', origin='lower', aspect='auto')
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

# 生成曼陀罗与声波结合的风格
def generate_mandala_waveform(y, output_path):
    plt.figure(figsize=(6, 6))
    radius = np.linspace(0, 2 * np.pi, len(y))
    plt.polar(radius, y[:len(radius)], color="black")
    plt.gca().set_theta_zero_location('N')
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

# 生成声波与文字结合的风格
def generate_wave_with_text(y, output_path):
    plt.figure(figsize=(6, 6))
    plt.plot(y, color="black")
    plt.text(0.5, 0.5, "Tattoo", ha='center', va='center', fontsize=15, color="black", transform=plt.gca().transAxes)
    plt.axis("off")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close()

# 生成图案的所有风格
def generate_all_styles(audio_path, output_folder, filename):
    try:
        y, sr = librosa.load(audio_path, sr=44100)
    except Exception as e:
        print(f"音频解析错误: {e}")
        return False

    # 限制数据长度
    y = y[:MAX_LENGTH]

    output_files = {}

    # 生成不同风格的纹身图案
    styles = {
        "wave": generate_waveform,
        "minimal": generate_minimal_waveform,
        "spectral": generate_spectral_waveform,
        "mandala_wave": generate_mandala_waveform,
        "wave_with_text": generate_wave_with_text,
    }

    for style, generator in styles.items():
        output_filename = f"{filename}_{style}.png"
        output_path = os.path.join(output_folder, output_filename)
        if style == "spectral":
            generator(y, sr, output_path)  # 频谱风格
        else:
            generator(y, output_path)  # 其他风格
        output_files[style] = output_filename

    return output_files
