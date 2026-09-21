import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf


def create_filters(sr):
    """
    FIR 201 taps.

    Low-pass  : cutoff 2 kHz
    High-pass : cutoff 300 Hz
    """

    numtaps = 201

    lowpass = signal.firwin(
        numtaps=numtaps,
        cutoff=2000,
        fs=sr,
        window="hamming"
    )

    highpass = signal.firwin(
        numtaps=numtaps,
        cutoff=300,
        fs=sr,
        pass_zero=False,
        window="hamming"
    )

    return lowpass, highpass


def apply_filters(y, sr):

    lowpass, highpass = create_filters(sr)

    y_low = signal.lfilter(
        lowpass,
        [1],
        y
    )

    y_high = signal.lfilter(
        highpass,
        [1],
        y
    )

    sf.write(
        "audio/filtered_lowpass_2k.wav",
        y_low,
        sr
    )

    sf.write(
        "audio/filtered_highpass_300.wav",
        y_high,
        sr
    )

    return lowpass, highpass, y_low, y_high


def plot_filter_response(lowpass, highpass, sr):

    f1, H1 = signal.freqz(
        lowpass,
        worN=4096,
        fs=sr
    )

    f2, H2 = signal.freqz(
        highpass,
        worN=4096,
        fs=sr
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        f1,
        20 * np.log10(
            np.maximum(np.abs(H1), 1e-10)
        ),
        label="Low-pass 2 kHz"
    )

    plt.plot(
        f2,
        20 * np.log10(
            np.maximum(np.abs(H2), 1e-10)
        ),
        label="High-pass 300 Hz"
    )

    plt.title("FIR Filter Frequency Response")

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")

    plt.xlim(
        0,
        min(10000, sr / 2)
    )

    plt.grid()
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "figures/filter_response.png",
        dpi=150
    )

    plt.show()


def plot_before_after(y, y_low, y_high, sr):

    nfft = 8192

    # Chỉ lấy 1 giây đầu để so sánh
    length = min(
        len(y),
        sr
    )

    original = y[:length]
    low = y_low[:length]
    high = y_high[:length]

    window = np.hamming(length)

    X = np.fft.rfft(
        original * window,
        n=nfft
    )

    L = np.fft.rfft(
        low * window,
        n=nfft
    )

    H = np.fft.rfft(
        high * window,
        n=nfft
    )

    freq = np.fft.rfftfreq(
        nfft,
        1 / sr
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        freq,
        20 * np.log10(np.maximum(np.abs(X), 1e-12)),
        label="Original"
    )

    plt.plot(
        freq,
        20 * np.log10(np.maximum(np.abs(L), 1e-12)),
        label="Low-pass"
    )

    plt.plot(
        freq,
        20 * np.log10(np.maximum(np.abs(H), 1e-12)),
        label="High-pass"
    )

    plt.xlim(
        0,
        min(10000, sr / 2)
    )

    plt.title(
        "Phổ trước và sau khi lọc"
    )

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")

    plt.legend()
    plt.grid()

    plt.tight_layout()

    plt.savefig(
        "figures/filter_before_after.png",
        dpi=150
    )

    plt.show()