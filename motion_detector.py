import numpy as np
import pandas as pd
from collections import deque
import os

class MotionDetector:
    def __init__(self, window_size=100, threshold=4.0):
        self.window = deque(maxlen=window_size)
        self.threshold = threshold
        self.last_state = None
        self.expected_len = None
        self.std_list = []  
        self.counter = 0  


    def update(self, csi_line: str):
        try:
            csi = np.array(list(map(int, csi_line.strip().strip("[]").split(","))))
            if len(csi) % 2 != 0:
                return None

            csi_complex = csi[::2] + 1j * csi[1::2]
            amplitude = np.abs(csi_complex)

            if self.expected_len is None and len(amplitude) > 57:
                self.expected_len = len(amplitude)
                print(f"[MotionDetector] Expected length: {self.expected_len}")
            if len(amplitude) != self.expected_len:
                return None

            self.window.append(amplitude)

            self.counter += 1
            if len(self.window) == self.window.maxlen and self.counter >= 50:
                self.counter = 0  # reset counter after processing a full window
                # print("window full!!!!!!!!!")
                window_array = np.stack(self.window)
                std = np.std(window_array, axis=0).mean()
                self.std_list.append(std)
                motion_detected = std > self.threshold
                self.last_state = motion_detected
                return motion_detected
            else:
                # print("window not full😡😠")
                return None  # not enough data to determine motion
        except Exception as e:
            print(f"[MotionDetector Error] {e}")
            return False


def read_csi_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['data'].tolist()

def main():
    dir_path = "/Users/yvonne/Documents/AIOT/comp7310_2025_group_project/benchmark/motion_detection/evaluation_motion"

    for file_name in sorted(os.listdir(dir_path)):
        if file_name.endswith(".csv"):
            file_path = os.path.join(dir_path, file_name)
            print(f"\n📂 Processing file: {file_name}")

            csi_lines = read_csi_data_from_csv(file_path)
            motion_detector = MotionDetector(window_size=100, threshold=4.0)

            true_count = 0
            total_count = 0

            for idx, csi_line in enumerate(csi_lines):
                result = motion_detector.update(csi_line)
                if result is not None:
                    total_count += 1
                    if result:
                        true_count += 1

            if total_count > 0:
                ratio = true_count / total_count
                print(f"📉 Minimum std during detection: {min(motion_detector.std_list):.6f}")
                print(f"📊 Detected True in {true_count} out of {total_count} frames.")
                print(f"✅ Motion Detected Ratio: {ratio:.2%}")
            else:
                print("⚠️ 没有有效的帧被处理（可能都是异常帧）。")

if __name__ == "__main__":
    main()