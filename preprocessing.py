import os
import json

import numpy as np


def calc_angele(vector_1, vector_2):
    if (vector_1[1] == vector_2[1]) and (vector_2[0] == vector_1[0]):
        return 0.0
    return np.arctan2(vector_2[1] - vector_1[1], vector_2[0] - vector_1[0])


def preapareDataOfFolder(path_to_folder, name_labels, labels, label_list, name_label_list, result, fixed_label=None):
    if os.path.exists(path_to_folder):
        json_files = [pos_json for pos_json in os.listdir(path_to_folder) if pos_json.endswith('.json')]
        if len(json_files) == 0:
            return name_labels, labels, label_list, name_label_list, result
        print('Found: ', len(json_files), 'json keypoint frame files')
        print('json files: ', json_files[0])
        elements = json_files[0].split('_')
        nameLabel = '_'.join(elements[0:2])
        label = elements[2]
        batch_size = 15

        sequence = []

        def add_label():
            if fixed_label is None:
                if label in label_list:
                    labels.append(label_list.index(label))
                else:
                    label_list.append(label)
                    labels.append(label_list.index(label))
            else:
                if fixed_label in label_list:
                    labels.append(label_list.index(fixed_label))
                else:
                    label_list.append(fixed_label)
                    labels.append(label_list.index(fixed_label))
            if nameLabel in name_label_list:
                name_labels.append(name_label_list.index(nameLabel))
            else:
                name_label_list.append(nameLabel)
                name_labels.append(name_label_list.index(nameLabel))

        for fileNum in range(len(json_files) - 1):
            try:
                temp_df1 = json.load(open(path_to_folder + json_files[fileNum]))
                temp_df2 = json.load(open(path_to_folder + json_files[fileNum + 1]))
            except Exception:
                print(path_to_folder + json_files[fileNum])
                continue

            try:
                np_v = np.array(temp_df1['people'][0]['pose_keypoints_2d'])
            except Exception:
                result.append(result[-1])
                add_label()
                continue
            np_v_reshape = np_v.reshape(int(len(np_v) / 3), 3)
            try:
                np_v2 = np.array(temp_df2['people'][0]['pose_keypoints_2d'])
            except Exception:
                if np_v is not None:
                    np_v2 = np_v
                else:
                    result.append(result[-1])
                    add_label()
                    continue
            np_v_reshape2 = np_v2.reshape(int(len(np_v2) / 3), 3)
            features = []

            # Ãœber die 14 Punkte des aktuellen und des nÃ¤chsten Frames gehen, hierbei Abstand und Winkel berechenen
            for i in range(15):
                point1 = np.array([np_v_reshape[i][0], np_v_reshape[i][1]])
                point2 = np.array([np_v_reshape2[i][0], np_v_reshape2[i][1]])
                # distance = np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 )
                distance = np.linalg.norm(point1 - point2)
                angle = calc_angele(point1, point2)
                probability = (np_v_reshape[i][2] + np_v_reshape2[i][2]) / 2
                features.append(float(distance))
                features.append(float(angle))
                features.append(float(probability))
            sequence.append(features)
            if len(sequence) >= batch_size:
                result.append(sequence)
                sequence = []
                add_label()
        if len(sequence) > 0:
            number_of_zero_features = batch_size - len(sequence)
            for n in range(number_of_zero_features):
                shape = len(sequence[0])
                zeros = []
                for t in range(shape):
                    zeros.append(.0)
                sequence.append(zeros)
            result.append(sequence)
            add_label()
    else:
        print(path_to_folder + " not found")
    return name_labels, labels, label_list, name_label_list, result
