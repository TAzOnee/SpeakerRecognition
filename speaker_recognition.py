#!/usr/bin/env python3

import os
import sys
import itertools
import glob
import argparse
from utils import read_wav
from interface import ModelInterface

def get_args():
    desc = "Speaker Recognition Command Line Tool"
    epilog = """
Wav files in each input directory will be labeled as the basename of the directory.
Note that wildcard inputs should be *quoted*, and they will be sent to glob.glob module.
Examples:
    Train (enroll a list of person named person*, and mary, with wav files under corresponding directories):
    ./speaker-recognition.py -t enroll -i "/tmp/person* ./mary" -m model.out
    python ./speaker-recognition.py -t enroll -i "./datatrain/hang/ datatrain/hoai/ datatrain/huong/ datatrain/nhung/ datatrain/tuananh datatrain/murray datatrain/jenny" -m model.out
    Predict (predict the speaker of all wav files):
    ./speaker-recognition.py -t predict -i "./*.wav" -m model.out
    python ./speaker-recognition.py -t predict -i "datatest/*.wav" -m model.out
"""
    parser = argparse.ArgumentParser(description=desc,epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t', '--task',
                       help='Task to do. Either "enroll" or "predict"',
                       required=False)

    parser.add_argument('-i', '--input',
                       help='Input Files(to predict) or Directories(to enroll)',
                       required=False)

    parser.add_argument('-m', '--model',
                       help='Model file to save(in enroll) or use(in predict)',
                       required=False)

    ret = parser.parse_args()
    return ret

def task_enroll(input_dirs, output_model):
    m = ModelInterface()
    input_dirs = [os.path.expanduser(k) for k in input_dirs.strip().split()]
    dirs = itertools.chain(*(glob.glob(d) for d in input_dirs))
    dirs = [d for d in dirs if os.path.isdir(d)]

    files = []
    if len(dirs) == 0:
        print ("No valid directory found!")
        sys.exit(1)

    for d in dirs:
        label = os.path.basename(d.rstrip('/'))
        wavs = glob.glob(d + '/*.wav')

        if len(wavs) == 0:
            print ("No wav file found in %s"%(d))
            continue
        for wav in wavs:
            try:
                fs, signal = read_wav(wav)
                m.enroll(label, fs, signal)
                print("wav %s has been enrolled"%(wav))
            except Exception as e:
                print(wav + " error %s"%(e))

    m.train()
    m.dump(output_model)

# def task_predict(input_files, input_model):
#     m = ModelInterface.load(input_model)
#     for f in glob.glob(os.path.expanduser(input_files)):
#         fs, signal = read_wav(f)
#         label, score = m.predict(fs, signal)
#         print (f, '->', label, ", score->", score)

def task_predict(path, input_model):
    m = ModelInterface.load(input_model)
    files = []
    sum,true = 0,0
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.wav' in file:
                files.append(os.path.join(r, file))
    for f in files:
        sum+=1
        fs, signal = read_wav(f)
        label, score = m.predict(fs, signal)
        strPath = os.path.realpath(f)
        y_true = os.path.basename(os.path.dirname(strPath))
        if (label==y_true):
           true+=1
        print (f, '->', label, ", score->", score)
    print('So file du doan dung: ',true)
    print('Tong so file: ', sum)
    print('accuracy: ',true/sum*100,'%')

def Predict_ByFile(file,input_model):
    print("start")
    m = ModelInterface.load(input_model)
    fs, signal = read_wav(file)
    print(fs)
    print(signal)
    label, score = m.predict(fs, signal)
    strPath = os.path.realpath(file)
    y_true = os.path.basename(os.path.dirname(strPath))
    print(label)
    print(score)
    return label
def OrderEnroll():
    m=ModelInterface.load("model.out")
    fs, signal = read_wav("./GUI/TotalRecording/18082020202755.wav")
    m.enroll("18082020202755", fs, signal)
    m.train()
    m.CheckEnroll()
    m.dump("mo1.out")
# def task_predictgui(path, input_model):
#     m = ModelInterface.load(input_model)
#     f=glob.glob(path)
#     fs, signal = read_wav(f[0])
#     label, score = m.predict(fs, signal)
#     return label
#
# if __name__ == "__main__":
#     # global args
#     # args = get_args()
#     #
#     # task = args.task
#     #
#     # if task == 'enroll':
#     #      task_enroll(args.input, args.model)
#     #
#     #
#     # elif task == 'predict':
#     #      task_predict(args.input, args.model)
#     #      task_predict("datatest/*.wav", "model1.out")
# task_enroll("./Train/*","model.out")
#
#      # task_predict("./Test", "model.out")
# Predict_ByFile("./GUI/TotalRecording/18082020202755.wav", "D:/doantotnghiep/Speaker_recognition/model.out")
# OrderEnroll()