import os

#path = "D:\doantotnghiep\speaker-recognition-py3-master\Test"
path = "datatest"
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.wav' in file:
            files.append(os.path.join(r, file))
for f in files:
    strPath = os.path.realpath(f)
    y_true = os.path.basename(os.path.dirname(strPath))
    print(y_true)
