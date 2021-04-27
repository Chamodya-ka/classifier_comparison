import mediapipe as mp 
import cv2
from pathlib import Path
import glob
import os
import numpy as np
import keras

def is_right_hand(kp):
    
    '''
    Returns True if kp is right hand and False if left hand.
    '''
    #MADE ALTERATION BECAUSE OF MIRRORED EFFECT
    digitgroups = [
        (17,18,19,20),
        (13,14,15,16),
        (9,10,11,12),
        (5,6,7,8),
        (2,3,4) # Thumb
    ]
    
    palm_dir_vec = np.array([0,0,0], dtype=np.float64)
    for digit in digitgroups:
        for idx in digit[1:]:
            palm_dir_vec += kp[idx] - kp[digit[0]]
            
    palm_pos_vec = np.array([0,0,0], dtype=np.float64)
    for digit in digitgroups:
        palm_pos_vec += kp[digit[0]]
    palm_pos_vec /= len(digitgroups)
    
    top_palm_pos_vec = kp[9]
    
    val = np.dot(np.cross(kp[2] - palm_pos_vec, palm_dir_vec), top_palm_pos_vec - palm_pos_vec)

    if val < 0: 
        print("RIGHT")
        return True
    
    return False


#os.chdir("/media/chamo/Backup Plus/WorkSpace/robocomp/ISL_Letters")
#os.chdir(os.path.abspath(__file__))
print(os.getcwd())
model = keras.models.load_model("./models/NN/II")
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands


letters = 'abcdefghiklmnopqrstuvwxyz'
train_to_test_ratio = 9

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
    static_image_mode=True,
    upper_body_only=True) as pose:

    with mp_hands.Hands(
    min_detection_confidence=0.6,
    static_image_mode=True,
    min_tracking_confidence=0.4) as hands:
      
      #f = open("csv_data/all_raw_csv_data.csv",'a') 
      while cap.isOpened():
    
        ret,image = cap.read()
        kp_lst = [0]*134
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results_pose = pose.process(image)
        results_hands = hands.process(image)

        # Draw the pose annotation on the image.
        #image.flags.writeable = True
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #mp_drawing.draw_landmarks(
        #    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        annotated_image = image.copy()
        if results_hands.multi_hand_landmarks:
          
          for hand_landmarks in results_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                  annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            #rows = []
            #row = a
            #point_list = []
            #is_right_hand()
            temp3d_kp_lst=[]
            temp2d_kp_lst=[]
            for coords in hand_landmarks.landmark:
                x,y,z= coords.x,coords.y,coords.z
                temp2d_kp_lst.append(x)
                temp2d_kp_lst.append(y)
                temp3d_kp_lst.append([x,y,z])
            if is_right_hand(np.array(temp3d_kp_lst)):
                kp_lst[0:42]=temp2d_kp_lst
            else:
                kp_lst[42:84]=temp2d_kp_lst
            

          
        if  results_pose.pose_landmarks:
          mp_drawing.draw_landmarks(annotated_image, results_pose.pose_landmarks, mp_pose.UPPER_BODY_POSE_CONNECTIONS)
          temppose_kp_lst=[]
        
          for pose_landmark in results_pose.pose_landmarks.landmark:

            temppose_kp_lst.append(pose_landmark.x)
            temppose_kp_lst.append(pose_landmark.y)
          
          
          kp_lst[84:]=temppose_kp_lst
        
        kp_lst= np.array(kp_lst)
        print(kp_lst.shape)
        kp_lst=np.expand_dims(kp_lst,0)
        print(kp_lst.shape)
        prediction = model.predict(kp_lst)
        
        guess = np.argmax(prediction)
        cv2.putText(annotated_image,str(letters[guess]) + ", confidence: " + str(round(prediction[0, guess] * 100, 2)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
            
          
        cv2.imshow('MediaPipe Pose', annotated_image)
        if cv2.waitKey(100) & 0xFF == 27:
          break


cap.release()
