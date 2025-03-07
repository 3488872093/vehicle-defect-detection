import cv2
import numpy as np
from PySide6.QtGui import QImage, Qt
from PySide6.QtCore import QThread, Signal


class Camera:
    def __init__(self, cam_preset_num=5):  # 限制检测范围为0到cam_preset_num-1
        self.cam_preset_num = cam_preset_num

    def get_cam_num(self):
        devices = []
        for device in range(self.cam_preset_num):
            stream = cv2.VideoCapture(device, cv2.CAP_DSHOW)
            if stream.isOpened():  # 直接检查摄像头是否能打开
                devices.append(device)
            stream.release()  # 释放资源
        return len(devices), devices


class WebcamThread(QThread):
    changePixmap = Signal(np.ndarray)

    def __init__(self, cam_id, parent=None):
        super().__init__(parent)
        self.cam_id = cam_id
        self.running = True
        self.cap = cv2.VideoCapture(self.cam_id, cv2.CAP_MSMF)  # 提前初始化摄像头
        if not self.cap.isOpened():
            print(f"Error: Could not open camera with ID {self.cam_id}")
            self.running = False

    def run(self):
        if not self.cap.isOpened():
            return  # If the camera couldn't be opened, exit the thread immediately.

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.changePixmap.emit(frame)
            else:
                print("Error: Failed to grab frame")
                break  # Exit the loop if frame grab fails

    def stop(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()  # 确保释放摄像头资源
        self.wait()  # 等待线程停止


if __name__ == '__main__':
    cam = Camera()
    cam_num, devices = cam.get_cam_num()
    print(f"Found {cam_num} camera(s): {devices}")

    if cam_num > 0:
        # 启动摄像头线程
        webcam_thread = WebcamThread(devices[0])
        webcam_thread.start()
    else:
        print("No cameras found.")
