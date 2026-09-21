1. THÔNG TIN TÍN HIỆU
----------------------------------------------------------------------
Sampling rate: 16000 Hz
Thời lượng: 30.00 s
Peak: 1.000000
RMS: 0.270255
Energy: 35058.082031
Clipping samples: 92

2. KẾT QUẢ LƯỢNG TỬ HÓA
----------------------------------------------------------------------
4-bit: SNR = 17.51 dB
8-bit: SNR = 41.57 dB
16-bit: SNR = inf dB

3. CÂU HỎI PHÂN TÍCH THÍ NGHIỆM
======================================================================

Câu 1 - Sampling / Resampling:
Alias có thể xuất hiện khi giảm sampling rate nếu tín hiệu chứa thành phần tần số lớn hơn tần số Nyquist mới. Khi giảm xuống 16 kHz, tần số Nyquist là 8 kHz; khi giảm xuống 8 kHz, tần số Nyquist chỉ còn 4 kHz. Nếu không lọc chống aliasing trước khi downsample, các thành phần vượt quá Nyquist có thể bị gập xuống vùng tần số thấp. Chất lượng nghe thường giảm rõ hơn ở 8 kHz do dải tần được giữ lại nhỏ hơn.

Câu 2 - Quantization:
Khi tăng số bit lượng tử hóa, số mức lượng tử tăng và bước lượng tử giảm, vì vậy sai số lượng tử giảm và SNR tăng. Trong thí nghiệm, SNR thực tế thu được là:
  - 4-bit: 17.51 dB
  - 8-bit: 41.57 dB
  - 16-bit: inf dB
Quantization noise thường dễ nghe rõ hơn ở những đoạn tín hiệu có biên độ nhỏ, vì lúc này công suất tín hiệu nhỏ trong khi mức nhiễu lượng tử vẫn tồn tại.

Câu 3 - FFT:
Với NFFT = 2048, độ rộng frequency bin là Δf = Fs/NFFT = 7.81 Hz.
Với NFFT = 8192, độ rộng frequency bin là Δf = Fs/NFFT = 1.95 Hz.
Khi tăng NFFT, khoảng cách giữa các frequency bin giảm nên phổ FFT được lấy mẫu dày hơn. Tuy nhiên, nếu độ dài frame không thay đổi thì độ phân giải tần số vật lý của tín hiệu không tự động tăng tương ứng. NFFT lớn chủ yếu giúp biểu diễn phổ mịn hơn và zero-padding nhiều hơn.

Câu 4 - Frame length:
Frame 10 ms có độ phân giải thời gian tốt hơn nhưng độ phân giải tần số thấp hơn. Frame 50 ms có độ phân giải tần số tốt hơn nhưng khả năng xác định chính xác thời điểm thay đổi của tín hiệu giảm. Frame 25 ms là sự cân bằng giữa hai yếu tố.

Câu 5 - Window:
Cửa sổ Hamming giảm spectral leakage tốt hơn cửa sổ Rectangular vì làm giảm sự gián đoạn tại hai đầu frame. Tuy nhiên Hamming làm main-lobe rộng hơn, vì vậy các đỉnh tần số nằm gần nhau có thể khó phân tách hơn. Rectangular có main-lobe hẹp hơn nhưng side-lobe lớn hơn.

Câu 6 - Filtering:
Đối với LPF 2 kHz, các thành phần tần số thấp được giữ lại trong khi các thành phần trên vùng cắt bị suy giảm. Đối với HPF 300 Hz, các thành phần thấp hơn vùng cắt bị suy giảm và các thành phần cao hơn được giữ lại. Do đó phổ sau lọc phải thay đổi phù hợp với đáp ứng tần số H(f) của từng bộ lọc.

Câu 7 - Coding:


4. CÂU HỎI BÁO CÁO
======================================================================

Câu 1. Giải thích bằng công thức tại sao Fs = 44.1 kHz chỉ biểu diễn độc lập đến 22.05 kHz.
Theo định lý Nyquist-Shannon, để biểu diễn chính xác một thành phần tần số Fmax cần Fs >= 2*Fmax. Vì vậy:
  Fmax = Fs / 2
       = 44100 / 2
       = 22050 Hz = 22.05 kHz.
Do đó với Fs = 44.1 kHz, miền tần số có thể biểu diễn độc lập chỉ đến 22.05 kHz. Thành phần cao hơn có thể gây aliasing nếu không được lọc trước khi lấy mẫu.

Câu 2. Nếu NFFT tăng từ 2048 lên 8192 nhưng frame vẫn dài 25 ms, điều gì thay đổi?
Với NFFT = 2048: Δf = 7.81 Hz/bin.
Với NFFT = 8192: Δf = 1.95 Hz/bin.
NFFT lớn làm khoảng cách giữa các bin nhỏ hơn và phổ được biểu diễn dày hơn. Tuy nhiên frame vẫn dài 25 ms nên lượng thông tin thực tế về độ phân giải tần số không tăng tương ứng. Phần tăng thêm chủ yếu là zero-padding.

Câu 3. Tại sao Hamming giảm spectral leakage nhưng có thể làm các đỉnh gần nhau khó phân tách?
Cửa sổ Rectangular tạo ra sự gián đoạn lớn tại biên frame, dẫn đến nhiều side-lobe và spectral leakage. Cửa sổ Hamming làm biên tín hiệu giảm dần nên side-lobe nhỏ hơn và leakage được giảm. Tuy nhiên Hamming làm main-lobe rộng hơn, do đó hai thành phần tần số rất gần nhau có thể bị chồng lên nhau và khó phân biệt.

Câu 4. FIR 201 taps tại 44.1 kHz có độ trễ bao nhiêu?
Với FIR tuyến tính đối xứng, độ trễ nhóm:
  Delay = (N - 1) / 2 samples
       = (201 - 1) / 2
       = 100 samples.
Tại Fs = 16000 Hz, độ trễ tương ứng khoảng 6.250 ms.
Độ trễ này tương đối nhỏ nhưng vẫn cần được xem xét trong các hệ thống xử lý thời gian thực, đặc biệt khi yêu cầu độ trễ rất thấp như tương tác trực tiếp hoặc xử lý tín hiệu theo thời gian thực.

Câu 5. Ảnh hưởng của B và sigma_x đến SNR lượng tử.
Với lượng tử hóa đều, bước lượng tử có dạng:
  Δ = 2 / 2^B
Công suất nhiễu lượng tử xấp xỉ:
  σq² = Δ² / 12
Do đó SNR tăng khi số bit B tăng. Với tín hiệu có mức RMS hoặc độ lệch chuẩn σx nhỏ, công suất tín hiệu giảm trong khi mức nhiễu lượng tử phụ thuộc vào bước lượng tử, nên SNR giảm. Đây là lý do tín hiệu có biên độ nhỏ dễ bộc lộ quantization noise hơn.

Câu 6. File WAV 16-bit stereo 44.1 kHz dài 60 s.
Công thức:
Size = Fs × bit_depth × channels × duration / 8
     = 44100 × 16 × 2 × 60 / 8
     = 10,584,000 bytes
     ≈ 10.584 MB.
Đây là kích thước PCM lý thuyết, chưa tính phần header của file WAV.


5. BIT RATE PCM
======================================================================
PCM hiện tại (16-bit, mono): 256,000 bit/s = 256.00 kbps.
