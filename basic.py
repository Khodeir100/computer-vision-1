import sys
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QVBoxLayout, QDialog, QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
import cv2

class ImageViewer(QDialog):
    def __init__(self) -> None:
        """Initialize"""
        super(ImageViewer, self).__init__()
        uic.loadUi('D:/Computer vision/Lec-2/new.ui', self)

        self.layout = QVBoxLayout(self)
        self.originview = QLabel(self)
        self.originview.setFixedSize(331, 331)
        self.layout.addWidget(self.originview)

        # Buttons
        self.button_open = QPushButton('Open Image', self)
        self.button_median = QPushButton('Apply Median Filter', self)
        self.button_canny = QPushButton('Apply Canny', self)
        self.button_save_median = QPushButton('Save Median Image', self)
        self.button_save_canny = QPushButton('Save Canny Image', self)
        
        self.layout.addWidget(self.button_open)
        self.layout.addWidget(self.button_median)
        self.layout.addWidget(self.button_canny)
        self.layout.addWidget(self.button_save_median)
        self.layout.addWidget(self.button_save_canny)

        # Connect buttons to methods
        self.button_open.clicked.connect(self.openFileDialog)
        self.button_median.clicked.connect(self.applyMedian)
        self.button_canny.clicked.connect(self.applyCanny)
        self.button_save_median.clicked.connect(self.saveMedianImage)
        self.button_save_canny.clicked.connect(self.saveCannyImage)

        self.img = None
        self.filtered_img = None  # To store the filtered image
        self.canny_img = None      # To store the Canny image

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                  "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)
        if fileName:
            self.img = cv2.imread(fileName)
            if self.img is not None:
                self.displayImage(self.img, self.originview)

    def applyMedian(self):
        if self.img is not None:
            # Apply Median Filter to reduce noise
            self.filtered_img = cv2.medianBlur(self.img, 5)  # Store the filtered image
            # Display the filtered image
            self.displayImage(self.filtered_img, self.originview)

    def applyCanny(self):
        if self.img is not None:
            if self.filtered_img is None:  # If median filter hasn't been applied, apply it first
                self.filtered_img = cv2.medianBlur(self.img, 5)
            # Convert to grayscale
            gray = cv2.cvtColor(self.filtered_img, cv2.COLOR_BGR2GRAY)
            # Apply Canny edge detection
            self.canny_img = cv2.Canny(gray, 100, 200)
            # Display the Canny image
            self.displayImage(self.canny_img, self.originview)

    def displayImage(self, img, label):
        if len(img.shape) == 2:  # If the image is grayscale
            height, width = img.shape
            bytesPerLine = width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        else:  # If the image is color
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        label.setPixmap(QPixmap.fromImage(qImg).scaled(label.size(), aspectRatioMode=1))

    def saveMedianImage(self):
        if self.filtered_img is not None:
            save_path = r"D:\Computer vision\Lec-2\1st pr. c.v\filtered_image.png"  # Specify path and filename
            cv2.imwrite(save_path, self.filtered_img)
            print(f"Filtered image saved to: {save_path}")

    def saveCannyImage(self):
        if self.canny_img is not None:
            save_path = r"D:\Computer vision\Lec-2\1st pr. c.v\canny_result.png"
            cv2.imwrite(save_path, self.canny_img)
            print(f"Canny image saved to: {save_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
