**NAO Robot Face Detection**

This Python script enables real-time face detection using the NAO robot's camera. It integrates OpenCV for face recognition with the NAOqi SDK to control the robot's camera, motion, and posture. The robot maintains a crouch position with a steady head orientation while streaming video, detecting faces using the Haar Cascade Classifier, and displaying the processed feed with bounding boxes around detected faces and a face count overlay.

**Features:**
Connects to a NAO robot via IP address and port.
Sets the robot to a crouch posture and keeps its head still.
Streams RGB video from the NAO camera in VGA resolution (640x480).
Detects faces in each frame and draws blue rectangles around them.
Displays the number of detected faces on the video feed.
Exits gracefully with 'q' key press, returning the robot to a rest position.

**Requirements:**
Python 3.x
OpenCV (cv2)
NAOqi SDK
NumPy
A NAO robot with network access

**Usage:**
Update the IP variable with your NAO robot's IP address.
Ensure the NAOqi SDK is installed and configured.
Run the script: python face_detection_nao.py.

**Notes:**
Tested with NAO robot firmware supporting NAOqi API.
Requires a stable network connection to the robot.
