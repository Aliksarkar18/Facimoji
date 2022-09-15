import cv2
from cvlearn import FaceMesh
from cvlearn.Utils import *
import numpy as np

cap = cv2.VideoCapture(0)

def draw_arc(img, x, y, rotation, radius):
    center = (x, y)
    axes = (radius, radius)
    angle = rotation
    startAngle = 100
    endAngle = 0

    cv2.ellipse(img, center, axes, angle, startAngle,
                endAngle, (255, 255, 255), int(radius/2))


detector = FaceMesh.FaceMeshDetector()
while True:
    _, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        for j in range(len(faces)):
            for i in range(len(faces[j])):
                faceLength, face_pos = findDistance(
                    faces[j][face['faceUp']], faces[j][face['faceDown']], img)

                cv2.ellipse(img, (face_pos[0], face_pos[1] - 30), (int(faceLength / 1.5), int(faceLength / 1.5) + 10),
                            find_rotation(
                                faces[j][face['faceUp']], faces[j][face['faceDown']]), 0, 360, (52, 225, 255),
                            -1)

                Right_eye_length, R_eye_pos = findDistance(
                    faces[j][rightEye['eyeUp']], faces[j][rightEye['eyeDown']], img)

                cv2.circle(img, (R_eye_pos[0], R_eye_pos[1]-30),
                           int(Right_eye_length/1.3), (65, 71, 100), -1)

                draw_arc(img, R_eye_pos[0] - 3, R_eye_pos[1] - 33, find_rotation(faces[j][rightEye['eyeRight']], faces[j] [rightEye['eyeLeft']]),
                         int(Right_eye_length/3))

                
                Left_eye_length, L_eye_pos = findDistance(faces[j][leftEye['eyeUp']], faces[j][leftEye['eyeDown']],
                                                          img)
                cv2.circle(img, (L_eye_pos[0], L_eye_pos[1] - 30),
                           int(Left_eye_length / 1.3), (65, 71, 100), -1)
                
                draw_arc(img, L_eye_pos[0] - 3, L_eye_pos[1] - 33, find_rotation(faces[j][leftEye['eyeRight']], faces[j] [leftEye['eyeLeft']]),
                         int(Left_eye_length/3))
               

                MouthLength1, Mouth_pos = findDistance(
                    faces[j][mouth['mouthRight']], faces[j][mouth['mouthLeft']], img)

                MouthLength2, _ = findDistance(
                    faces[j][mouth['mouthUp']], faces[j][mouth['mouthDown']], img)

                cv2.ellipse(img, (Mouth_pos[0], Mouth_pos[1] - 30), (int(MouthLength1 / 1.6), int(MouthLength2)),
                            find_rotation(faces[j][mouth['mouthRight']], faces[j][mouth['mouthLeft']]), 360, 180, (0, 60, 255), -1)

                if MouthLength2 >= 30:
                    cv2.ellipse(img, (Mouth_pos[0], Mouth_pos[1] - 30), (int(MouthLength1 / 1.6)-10,-20),
                            find_rotation(faces[j][mouth['mouthRight']], faces[j][mouth['mouthLeft']]), 360, 180, (255, 255, 255), -1)
                    
                right_eyebrow = [
                    [faces[j][336][0], faces[j][336][1] - 40],
                    [faces[j][296][0], faces[j][296][1] - 40],
                    [faces[j][334][0], faces[j][334][1] - 40],
                    [faces[j][293][0], faces[j][293][1] - 40],
                    [faces[j][300][0], faces[j][300][1] - 40],
                    [faces[j][283][0], faces[j][283][1] - 40],
                    [faces[j][282][0], faces[j][282][1] - 40],
                    [faces[j][295][0], faces[j][295][1] - 40],
                    [faces[j][285][0], faces[j][285][1] - 40]
                ]
                right_eyebrow_polygon = np.array([right_eyebrow], np.int32)
                cv2.fillPoly(img, pts=[right_eyebrow_polygon], color=(0, 0, 0))

                left_eyebrow = [
                    [faces[j][70][0], faces[j][70][1] - 40],
                    [faces[j][63][0], faces[j][63][1] - 40],
                    [faces[j][105][0], faces[j][105][1] - 40],
                    [faces[j][66][0], faces[j][66][1] - 40],
                    [faces[j][107][0], faces[j][107][1] - 40],
                    [faces[j][55][0], faces[j][55][1] - 40],
                    [faces[j][65][0], faces[j][65][1] - 40],
                    [faces[j][52][0], faces[j][52][1] - 40],
                    [faces[j][53][0], faces[j][53][1] - 40],
                ]
                left_eyebrow_polygon = np.array([left_eyebrow], np.int32)
                cv2.fillPoly(img, pts=[left_eyebrow_polygon], color=(0, 0, 0))

    cv2.imshow('img', img)
    cv2.waitKey(7)