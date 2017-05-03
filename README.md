# mytesting
This is my testing and examples workbench


# mycamtest

Simple, yet capable motion detecting by video camera.
The code is copied from great article found at:
http://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/

I only added minor fixes such as:
* resetting the initial frame every N frames to avoid perpetual motion detection after camera moves or if initial frame is blank or imperfect

## Setup and run
1. Install, setup and confirm your computer video camera is working and is capable of viewing. Use other tools to confirm it is operable.
2. Install OPENCV http://opencv.org/ python library. This is the cornerstone of entire 'simplicity' here. Use `pip install opencv-python`
3. Run the script: `python src\camtest.py`
4. At this point, observe three windows containing camera capture with annotated moving area, and differential frames demonstrating how the detection is done.

