# NLP-Dataset-Collection-Scripts
Python scripts to speed up the voice recording and segmentation process for NLP dataset collection using a GUI. Buit at [Swaayatt Robots](http://swaayatt-robots.com) during my freshman summer internship 2017.

## voicedatacollection.py
This script was built to use a simple GUI guidance instead of the manual ticking and counting on a wrist watch. A number of classes for which the dataset had to be collected 100 times were listed in the source code and they pop up with a counter with the automatic playback and the manual option to replay the sound, re-record the sound and going for the next recording. The script under the hood does the shell utility work of creating the directories and later on, it becomes quite easier to input the audio segments for training using the similar pattern of the paths.

## trim_wav.py
Initially, the voices were recorded in a single `.wav` file and the splitting was being done manually. I thought of a GUI script to segment those audio files based on trimming at silence for a determined threshold value of noise. 

These scripts can be hacked further to remove anything that is manual or require the user input. But doing this way, one may get arbitary audio segment(s) that are not useful. 
