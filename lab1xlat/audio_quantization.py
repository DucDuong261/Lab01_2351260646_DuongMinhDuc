import numpy as np
import librosa
import soundfile as sf
import matplotlib.pyplot as plt


# ============================================================
# QUANTIZATION
# ============================================================

def quantize(y, bits):

    levels = 2 ** bits

    step = 2 / levels

    y = np.clip(y, -1, 1)

    y_quantized = (
        np.round((y + 1) / step)
        * step
        - 1
    )

    y_quantized = np.clip(
        y_quantized,
        -1,
        1
    )

    return y_quantized


def calculate_snr(y, y_quantized):

    error = y_quantized - y

    signal_power = np.sum(y ** 2)

    noise_power = np.sum(error ** 2)

    return 10 * np.log10(
        signal_power / noise_power
    )


def quantization_experiment(y, sr):

    results = []

    for bits in [4, 8, 16]:

        yq = quantize(
            y,
            bits
        )

        snr = calculate_snr(
            y,
            yq
        )

        print(
            f"{bits} bit -> "
            f"SNR = {snr:.2f} dB"
        )

        sf.write(
            f"audio/quantized_{bits}bit.wav",
            yq,
            sr
        )

        results.append(
            (bits, snr)
        )

    return results


def plot_snr(results):

    bits = [
        r[0]
        for r in results
    ]

    snr = [
        r[1]
        for r in results
    ]

    plt.figure(figsize=(7, 5))

    plt.plot(
        bits,
        snr,
        marker="o"
    )

    plt.title(
        "SNR theo số bit lượng tử hóa"
    )

    plt.xlabel(
        "Bits / sample"
    )

    plt.ylabel(
        "SNR (dB)"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "figures/quantization_snr.png",
        dpi=150
    )

    plt.show()


# ============================================================
# RESAMPLING
# ============================================================

def resample_audio(y, sr):

    for target_sr in [16000, 8000]:

        y_resampled = librosa.resample(
            y.astype(np.float32),
            orig_sr=sr,
            target_sr=target_sr
        )

        sf.write(
            f"audio/resampled_{target_sr}Hz.wav",
            y_resampled,
            target_sr
        )

        print(
            f"Resampled: {sr} Hz -> "
            f"{target_sr} Hz"
        )


# ============================================================
# PCM BIT RATE
# ============================================================

def calculate_pcm(sr, bits, channels, duration):

    bitrate = (
        sr
        * bits
        * channels
    )

    size_bytes = (
        bitrate
        * duration
        / 8
    )

    size_mb = (
        size_bytes
        / (1024 ** 2)
    )

    print("\n===== PCM =====")

    print(
        f"Bit rate : "
        f"{bitrate / 1000:.2f} kbps"
    )

    print(
        f"Size     : "
        f"{size_mb:.2f} MB"
    )

    return bitrate, size_mb