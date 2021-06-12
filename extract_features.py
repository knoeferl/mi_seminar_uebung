import os
from sys import platform
import subprocess
import csv

path_ = "./aufnahmen/"

errors = []


def create_json_and_mp4(filename, path):
    input_file = os.path.realpath(os.path.curdir) + "/" + path + "/" + filename
    print(input_file)
    base, ext = os.path.splitext(filename)
    try:
        json_folder = os.path.realpath(os.path.curdir) + "/data_aufnahme_json/" + base + "_json/"
        mp4_file = json_folder + filename
        rotated = mp4_file + "_rotated.avi"
        avi_ = mp4_file + ".avi"
        # if not path.exists(json_folder):
        os.makedirs(json_folder, exist_ok=True)
        print(avi_)
        subprocess.run(["ffmpeg\\bin\\ffmpeg.exe", "-y", "-loglevel", "info",
                        "-i", input_file, rotated,  "-vf", 'transpose=1'], shell=True,
                       capture_output=True, check=True)
        subprocess.run(
            ["bin\\OpenPoseDemo.exe", "--video", rotated, "--face", "--hand", "--write_json",
             json_folder, "--display", "0", "--write_video", avi_], shell=True, capture_output=True,
            check=True,
            cwd="openpose")
        print("Openpose finished!")
    except Exception as e:
        errors.append(input_file)
        return
    # if not path.exists(mp4_file):
    subprocess.run(["ffmpeg\\bin\\ffmpeg.exe", "-y", "-loglevel", "info", "-i", avi_, mp4_file], shell=True,
                   capture_output=True, check=True)
    print("mp4 created")
    return mp4_file, json_folder


if __name__ == "__main__":
    for subfile_ in os.listdir(path_):
        if not os.path.isdir(path_ + "/" + subfile_):
            create_json_and_mp4(subfile_, path_)

    with open('failed_jsons.csv', 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(errors)
