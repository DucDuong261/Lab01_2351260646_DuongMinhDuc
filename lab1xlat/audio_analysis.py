import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import signal


# ============================================================
# A. ĐỌC AUDIO
# ============================================================

def load_audio(audio_path):
    """
    Đọc file WAV/MP3 và giữ nguyên sampling rate.
    """
    y, sr = librosa.load(audio_path, sr=None, mono=True)

    duration = len(y) / sr

    print("===== AUDIO INFORMATION =====")
    print(f"Sampling rate : {sr} Hz")
    print(f"Duration      : {duration:.2f} s")
    print(f"Channels      : 1 (mono)")
    print(f"Samples       : {len(y):,}")

    return y, sr


def normalize_audio(y):
    """
    Chuẩn hóa biên độ về [-1, 1].
    """
    peak = np.max(np.abs(y))

    if peak == 0:
        return y

    return y / peak


# ============================================================
# B. TIME DOMAIN
# ============================================================

def calculate_time_features(y):
    peak = np.max(np.abs(y))
    rms = np.sqrt(np.mean(y ** 2))
    energy = np.sum(y ** 2)

    clipping = np.sum(np.abs(y) >= 0.999)

    print("\n===== TIME DOMAIN =====")
    print(f"Peak           : {peak:.6f}")
    print(f"RMS            : {rms:.6f}")
    print(f"Energy         : {energy:.2f}")
    print(f"Clipping sample: {clipping}")

    return peak, rms, energy


def plot_waveform(y, sr):
    time = np.arange(len(y)) / sr

    plt.figure(figsize=(12, 4))
    plt.plot(time, y, linewidth=0.5)

    plt.title("Waveform toàn bộ bài hát")
    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")
    plt.grid()

    plt.tight_layout()
    plt.savefig("figures/waveform.png", dpi=150)
    plt.show()


def plot_waveform_segment(y, sr, start=0, duration=1):
    start_sample = int(start * sr)
    end_sample = int((start + duration) * sr)

    segment = y[start_sample:end_sample]

    time = np.arange(len(segment)) / sr + start

    plt.figure(figsize=(12, 4))
    plt.plot(time, segment)

    plt.title(f"Waveform {start}s - {start + duration}s")
    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")
    plt.grid()

    plt.tight_layout()
    plt.savefig("figures/waveform_segment.png", dpi=150)
    plt.show()


# ============================================================
# C. FFT
# ============================================================

def fft_analysis(y, sr, start=0, duration=1, nfft=4096):
    """
    FFT trên một đoạn 0.5-1 giây.
    Dùng Hamming window theo yêu cầu Lab.
    """

    start_sample = int(start * sr)
    end_sample = int((start + duration) * sr)

    segment = y[start_sample:end_sample]

    # Hamming window
    window = np.hamming(len(segment))
    segment = segment * window

    # FFT
    X = np.fft.rfft(segment, n=nfft)

    # Frequency axis
    freq = np.fft.rfftfreq(nfft, 1 / sr)

    magnitude = np.abs(X)

    magnitude_db = 20 * np.log10(
        np.maximum(magnitude, 1e-12)
    )

    delta_f = sr / nfft

    print("\n===== FFT =====")
    print(f"NFFT           : {nfft}")
    print(f"Frequency bin  : {delta_f:.3f} Hz")

    # Tìm peak
    peaks, _ = signal.find_peaks(
        magnitude,
        distance=20
    )

    # Lấy 3 peak lớn nhất
    if len(peaks) > 0:
        peaks = peaks[
            np.argsort(magnitude[peaks])[-3:]
        ]

        peaks = peaks[::-1]

        print("Top spectral peaks:")

        for p in peaks:
            print(f"  {freq[p]:.2f} Hz")

    return freq, magnitude, magnitude_db


def plot_fft(freq, magnitude, magnitude_db):
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)

    plt.plot(freq, magnitude)

    plt.title("FFT - Magnitude Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")

    plt.xlim(0, min(10000, freq[-1]))

    plt.grid()

    plt.subplot(2, 1, 2)

    plt.plot(freq, magnitude_db)

    plt.title("FFT - Magnitude Spectrum (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")

    plt.xlim(0, min(10000, freq[-1]))

    plt.grid()

    plt.tight_layout()

    plt.savefig("figures/fft.png", dpi=150)

    plt.show()


def compare_nfft(y, sr, start=0, duration=1):

    start_sample = int(start * sr)
    end_sample = int((start + duration) * sr)

    segment = y[start_sample:end_sample]

    segment = segment * np.hamming(len(segment))

    plt.figure(figsize=(12, 6))

    for nfft in [2048, 8192]:

        X = np.fft.rfft(segment, n=nfft)

        freq = np.fft.rfftfreq(
            nfft,
            1 / sr
        )

        magnitude_db = 20 * np.log10(
            np.maximum(np.abs(X), 1e-12)
        )

        plt.plot(
            freq,
            magnitude_db,
            label=f"NFFT={nfft}, Δf={sr/nfft:.2f} Hz"
        )

    plt.xlim(0, min(10000, sr / 2))

    plt.title("So sánh NFFT")

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")

    plt.legend()
    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "figures/fft_nfft_comparison.png",
        dpi=150
    )

    plt.show()


# ============================================================
# D. STFT
# ============================================================

def plot_spectrogram(y, sr):

    frame_sizes = [10, 25, 50]

    plt.figure(figsize=(12, 10))

    for i, frame_ms in enumerate(frame_sizes):

        nperseg = int(frame_ms / 1000 * sr)

        hop = int(0.010 * sr)

        f, t, Z = signal.stft(
            y,
            fs=sr,
            window="hamming",
            nperseg=nperseg,
            noverlap=nperseg - hop,
            nfft=2048
        )

        magnitude_db = 20 * np.log10(
            np.maximum(np.abs(Z), 1e-12)
        )

        plt.subplot(3, 1, i + 1)

        plt.pcolormesh(
            t,
            f,
            magnitude_db,
            shading="auto"
        )

        plt.title(
            f"STFT - Frame {frame_ms} ms / Hop 10 ms"
        )

        plt.xlabel("Time (s)")
        plt.ylabel("Frequency (Hz)")

        plt.ylim(0, min(10000, sr / 2))

    plt.tight_layout()

    plt.savefig(
        "figures/spectrogram.png",
        dpi=150
    )

    plt.show()


# ============================================================
# E. WINDOW EXPERIMENT
# ============================================================

def compare_windows(y, sr, start=0, duration=1):

    start_sample = int(start * sr)
    end_sample = int((start + duration) * sr)

    segment = y[start_sample:end_sample]

    nfft = 8192

    rectangular = np.ones(len(segment))
    hamming = np.hamming(len(segment))

    X_rect = np.fft.rfft(
        segment * rectangular,
        n=nfft
    )

    X_hamming = np.fft.rfft(
        segment * hamming,
        n=nfft
    )

    freq = np.fft.rfftfreq(
        nfft,
        1 / sr
    )

    rect_db = 20 * np.log10(
        np.maximum(np.abs(X_rect), 1e-12)
    )

    hamming_db = 20 * np.log10(
        np.maximum(np.abs(X_hamming), 1e-12)
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        freq,
        rect_db,
        label="Rectangular"
    )

    plt.plot(
        freq,
        hamming_db,
        label="Hamming"
    )

    plt.xlim(0, min(10000, sr / 2))

    plt.title(
        "So sánh Rectangular và Hamming"
    )

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")

    plt.legend()
    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "figures/window_comparison.png",
        dpi=150
    )

    plt.show()