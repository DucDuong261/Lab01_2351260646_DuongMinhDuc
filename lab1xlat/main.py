import os

from audio_analysis import (
    load_audio,
    normalize_audio,
    calculate_time_features,
    plot_waveform,
    plot_waveform_segment,
    fft_analysis,
    plot_fft,
    compare_nfft,
    plot_spectrogram,
    compare_windows
)

from audio_filter import (
    create_filters,
    apply_filters,
    plot_filter_response,
    plot_before_after
)

from audio_quantization import (
    quantization_experiment,
    plot_snr,
    resample_audio,
    calculate_pcm
)


# ============================================================
# CẤU HÌNH
# ============================================================

AUDIO_FILE = r"D:\Bob\TaiLieuHoc\SpokenLanguage\LyricsSearch\dataset\snippets\_XX248bq6Pw.wav"


os.makedirs("audio", exist_ok=True)
os.makedirs("figures", exist_ok=True)


# ============================================================
# A. ĐỌC AUDIO
# ============================================================

print("\n")
print("=" * 60)
print("A. ĐỌC VÀ KIỂM TRA AUDIO")
print("=" * 60)

y, sr = load_audio(AUDIO_FILE)

y = normalize_audio(y)


# ============================================================
# B. TIME DOMAIN
# ============================================================

print("\n")
print("=" * 60)
print("B. PHÂN TÍCH MIỀN THỜI GIAN")
print("=" * 60)

peak, rms, energy = calculate_time_features(y)

plot_waveform(y, sr)

plot_waveform_segment(
    y,
    sr,
    start=0,
    duration=1
)


# ============================================================
# C. FFT
# ============================================================

print("\n")
print("=" * 60)
print("C. FFT")
print("=" * 60)

# Nếu bài hát dài hơn 46s:
# lấy đoạn 45-46s giống case study trong đề.
# Nếu ngắn hơn thì lấy đoạn đầu.

if len(y) >= 46 * sr:
    fft_start = 45
else:
    fft_start = 0


freq, magnitude, magnitude_db = fft_analysis(
    y,
    sr,
    start=fft_start,
    duration=1,
    nfft=4096
)

plot_fft(
    freq,
    magnitude,
    magnitude_db
)


# So sánh NFFT 2048 và 8192
compare_nfft(
    y,
    sr,
    start=fft_start,
    duration=1
)


# ============================================================
# D. STFT
# ============================================================

print("\n")
print("=" * 60)
print("D. STFT / SPECTROGRAM")
print("=" * 60)

plot_spectrogram(
    y,
    sr
)


# ============================================================
# E. WINDOW
# ============================================================

print("\n")
print("=" * 60)
print("E. RECTANGULAR vs HAMMING")
print("=" * 60)

compare_windows(
    y,
    sr,
    start=fft_start,
    duration=1
)


# ============================================================
# F. FIR FILTER
# ============================================================

print("\n")
print("=" * 60)
print("F. FIR FILTER")
print("=" * 60)

lowpass, highpass, y_low, y_high = apply_filters(
    y,
    sr
)

plot_filter_response(
    lowpass,
    highpass,
    sr
)

plot_before_after(
    y,
    y_low,
    y_high,
    sr
)


# ============================================================
# G. QUANTIZATION
# ============================================================

print("\n")
print("=" * 60)
print("G. QUANTIZATION")
print("=" * 60)

results = quantization_experiment(
    y,
    sr
)

plot_snr(
    results
)


# ============================================================
# G. RESAMPLING
# ============================================================

print("\n")
print("=" * 60)
print("G. RESAMPLING")
print("=" * 60)

resample_audio(
    y,
    sr
)


# ============================================================
# G. PCM
# ============================================================

duration = len(y) / sr

calculate_pcm(
    sr=sr,
    bits=16,
    channels=1,
    duration=duration
)


print("\n")
print("=" * 60)
print("ĐÃ HOÀN THÀNH LAB 1")
print("=" * 60)