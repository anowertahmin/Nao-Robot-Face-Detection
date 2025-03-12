import cv2
import numpy as np
from naoqi import ALProxy

IP = "169.254.20.117"  # Replace with your NAO robot's IP address
PORT = 9559

class FaceRecognition:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame, len(faces)

def main():
    # Create proxies
    video_proxy = ALProxy("ALVideoDevice", IP, PORT)
    motion_proxy = ALProxy("ALMotion", IP, PORT)
    posture_proxy = ALProxy("ALRobotPosture", IP, PORT)

    # Set robot to crouch position
    posture_proxy.goToPosture("Crouch", 1.0)

    # Keep head still
    motion_proxy.setStiffnesses("Head", 1.0)
    motion_proxy.setAngles("HeadYaw", 0.0, 0.1)
    motion_proxy.setAngles("HeadPitch", 0.0, 0.1)

    resolution = 2    # VGA
    color_space = 11  # RGB

    # Subscribe to the camera
    capture_device = video_proxy.subscribeCamera("python_client", 0, resolution, color_space, 30)

    face_recognition = FaceRecognition()

    while True:
        # Keep head still
        motion_proxy.setAngles("HeadYaw", 0.0, 0.1)
        motion_proxy.setAngles("HeadPitch", 0.0, 0.1)

        # Get image from NAO camera
        nao_image = video_proxy.getImageRemote(capture_device)

        # Get the image size and pixel array
        width = nao_image[0]
        height = nao_image[1]
        array = nao_image[6]

        # Create a numpy array from the pixel array
        frame = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))

        # Process the frame to detect faces
        frame, face_count = face_recognition.process_frame(frame)

        # Display the number of faces detected
        cv2.putText(frame, "Faces: {}".format(face_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Display the frame
        cv2.imshow("NAO Camera", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Unsubscribe from the camera
    video_proxy.unsubscribe(capture_device)

    # Close all OpenCV windows
    cv2.destroyAllWindows()

    # Return to rest position
    posture_proxy.goToPosture("Rest", 1.0)

if __name__ == "__main__":
    main()