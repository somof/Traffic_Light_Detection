PYTHON = ~/.pyenv/versions/2.7.12/bin/python
PIP = ~/.pyenv/versions/2.7.12/bin/pip

PYTHONC = ~/.pyenv/versions/3.6.4/bin/python
PIPC = ~/.pyenv/versions/3.6.4/bin/pip

PYTHON = env LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64 ~/.pyenv/versions/2.7.12/bin/python

all: 
	$(PYTHONC) infer.py
	ffmpeg -r 30 -i predict/res%06d.png -vcodec libx264 -pix_fmt yuv420p -r 60 ../ssd_video_epoch70sup5.mp4

infer:
	$(PYTHON) SSD_infer.py

train:
	$(PYTHON) SSD_train.py

view:
	$(PYTHONC) view.supp.py
	#$(PYTHON) view_pickle.py

install:
	cat install_package.txt | xargs $(PIP) install
