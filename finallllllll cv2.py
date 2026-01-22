import cv2
import mediapipe as mp
import math
import tkinter as tk
from tkinter import filedialog

def calculate_angle(a, b, c):
    ba = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]
    
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)
    
    if mag_ba * mag_bc == 0:
        return 0
    
    angle_rad = math.acos(dot_product / (mag_ba * mag_bc))
    angle_deg = angle_rad * (180.0 / math.pi)
    return angle_deg

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def choose_video():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(title="اختر ملف الفيديو", filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    return file_path

def draw_feedback(image, left_knee_correct, right_knee_correct):
    height, width = image.shape[:2]
    
    left_color = (0, 255, 0) if left_knee_correct else (0, 0, 255)
    left_text = "Left Knee: High" if left_knee_correct else "Left Knee: Low"
    
    cv2.rectangle(image, (20, 20), (300, 60), left_color, -1)
    cv2.putText(image, left_text, (30, 45), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    right_color = (0, 255, 0) if right_knee_correct else (0, 0, 255)
    right_text = "Right Knee: High" if right_knee_correct else "Right Knee: Low"
    
    cv2.rectangle(image, (20, 70), (300, 110), right_color, -1)
    cv2.putText(image, right_text, (30, 95), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def analyze_high_knees(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("خطأ في فتح ملف الفيديو.")
        return

    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (960, 540))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = results.pose_landmarks.landmark

                # نقاط الجسم المهمة لتحليل تمرين الهاينيز
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * image.shape[1],
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image.shape[0]]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * image.shape[1],
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * image.shape[0]]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * image.shape[1],
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * image.shape[0]]
                
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * image.shape[1],
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * image.shape[0]]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * image.shape[1],
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * image.shape[0]]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * image.shape[1],
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * image.shape[0]]

                left_knee_angle = calculate_angle(left_ankle, left_knee, left_hip)
                right_knee_angle = calculate_angle(right_ankle, right_knee, right_hip)

                left_knee_correct = left_knee_angle < 90  
                right_knee_correct = right_knee_angle < 90

               
                cv2.putText(image, f'L Knee Angle: {left_knee_angle:.1f}°', 
                            (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                            (0, 255, 0) if left_knee_correct else (0, 0, 255), 1)
                cv2.putText(image, f'R Knee Angle: {right_knee_angle:.1f}°', 
                            (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                            (0, 255, 0) if right_knee_correct else (0, 0, 255), 1)

                cv2.line(image, (int(left_ankle[0]), int(left_ankle[1])), 
                        (int(left_knee[0]), int(left_knee[1])), 
                        (0, 255, 255), 2)
                cv2.line(image, (int(right_ankle[0]), int(right_ankle[1])), 
                        (int(right_knee[0]), int(right_knee[1])), 
                        (0, 255, 255), 2)

               
                draw_feedback(image, left_knee_correct, right_knee_correct)

            cv2.imshow("AI Trainer - High Knees Analysis", image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_file = choose_video()
    if video_file:
        analyze_high_knees(video_file)
