Description
=======================
These are stable programs of Randomforest-based Database Unmixing (Mizuochi et al., 2018), written in python languages. It has been tested for Python 2.7.12 on Linux system (Ubuntu 16.04).

### Revision History:
First release on 2018/07/18: original version (Mizuochi et al., 2018)

### References:
1. Mizuochi, H., Nishiyama, C., Ridwansyah, I., Nasahara, K. N. (2018): Monitoring of an Indonesian tropical wetland by machine-learning-based data fusion of passive and active microwave sensors. Remote Sensing. 10(8), 1235, pp. 1-19.

How to Use
=====================

### Preparation:
Before running program, the following preparation is required.

##### A) install the following modules for python.
        - sklearn.ensamble (http://scikit-learn.org/stable/modules/ensemble.html#forest).
        - multiprocessing (https://docs.python.org/3/library/multiprocessing.html)
        - numpy (https://docs.scipy.org/doc/numpy-1.13.0/user/index.html)

##### B) Make input directory and place the following input maps there.

        - temporally frequent maps ("T maps" hereafter) and spatially fine maps ("S maps" hereafter).
          data format is 2 bytes Integer. All maps must be co-registered and be the same size.
          Any filenames are acceptable. for example, S map and T map for a year "YYYY" and a day of year "DOY" can be:
          "spatial_YYYYDOY.raw", "temporal_YYYYDOY.raw".

##### C) Put the following list files in the same directory as the program (RFDBUX.py).
        - namelist of T map and S map pairs. Each map name must be separated by a separator "," and T map name must be before S map name.
                        e.g."pairlist.txt"
                        temporal_2002001.raw,spatial_2002001.raw
                        temporal_2002001.raw,spatial_2002002.raw
                        temporal_2002001.raw,spatial_2002005.raw
                        temporal_2002001.raw,spatial_2002007.raw
                        ...

        - namelist of T map and predicted S map (output). Each map name must be separated by a separator "," and T map name must be before the predicted S map name.
                        e.g."predlist.txt"
                        temporal_2002001.raw,spatial_2002001_comp_rf.raw
                        temporal_2002002.raw,spatial_2002002_comp_rf.raw
                        temporal_2002003.raw,spatial_2002003_comp_rf.raw
                        ...

##### D) Make sure you know all the following parameters, which will be given as arguments when you run the program.
	in_dir //absolute path of the directory where input maps are placed.
	out_dir //absolute path of the directory where predicted maps will be written.
	pairlist_name //list of input pairs (e.g. pairlist.txt) that is placed in the same directory of this python script.
	predlist_name //list of prediction (e.g. predlist.txt) that is placed in the same directory of this python script.
	NTREES //number of decision trees used in random forest. 
	MINNODESIZE //minimum size of samples for each decision tree nodes.
	Maxlevel //maximum level of decision tree nodes.
	COL //number of columns of a map.
	ROW //number of rows of a map.
	NV //null value. must NOT be in between valid range of S and T data.
	MULTI //number of CPU cores which will be used for multiprocessing.

### Execute:

	$python RFDBUX.py in_dir out_dir pairlist_name predlist_name NTREES MINNODESIZE Maxlevel COL ROW NV MULTI

The predicted S maps will be written under your determined output directory.
