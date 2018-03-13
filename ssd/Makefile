PYTHON = ~/.pyenv/versions/2.7.12/bin/python
PIP = ~/.pyenv/versions/2.7.12/bin/pip
#PYTHON = env LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64 ~/.pyenv/versions/3.5.2/bin/python3.5
#PYTHON = env LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64 ~/.pyenv/versions/2.7.12/bin/python

PYTHON = ~/.pyenv/versions/3.6.4/bin/python
PIP = ~/.pyenv/versions/3.6.4/bin/pip

all: 
	@#$(PYTHON) run_ssd.py
	$(PYTHON) SSD_infer.py

train:
	$(PYTHON) SSD_train.py

view:
	$(PYTHON) view_pickle.py

install:
	cat install_package.txt | xargs $(PIP) install
