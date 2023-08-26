# PHYS5020_SimpleITK_MRI
PHYS5020 SimpleITK and MRI Assignment Code and Data


In this assignment, you will write Python code to process MRI images provided to you in DICOM format. These images were acquired as part of regular MRI scanner QA on a Large ACR phantom. You will first write code in Python to read DICOM files, extract relevant DICOM tags and perform four QA tests. The ACR MRI QA manual is provided to you and contains details of the image series and slices as well as the formulae that are to be used to perform the tests. The code framework is already provided to you with pseudo code describing the required steps. Complete missing code as needed. You can also write your own code from scratch if you wish. Complete the questions below and upload your answer sheet on Canvas. Please do not submit your code.

Requirements:
Python 3.x installation
Libraries - numpy, scipy, SimpleITK, os, glob, tqdm and matplotlib  

Python code: 
You are provided with the code framework for this assignment. Some of the function definitions and some lines in the code have been taken out and are for you to complete. 

Imaging data:
1.	Localiser – This is a single, sagittal image slice acquired through the center of the phantom. 
2.	ACR_T1 – This is an axial series of 11 T1-weighted images acquired using ACR scan protocol. 
3.	ACR_T2 – This is an axial series of 44 T2-weighted images acquired using the ACR scan protocol. Each set of 11 T2-weighted images are acquired with a different TE. A total of 4 TEs are used. 
4.	Site_T1 – This is an axial series of 11 T1-weighted images acquired using a site-specific protocol.
5.	Site_T2 – This is an axial series of 11 T2-weighted images acquired using a site-specific protocol.
6.	T2_map – This is a T2 map calculated by the scanner using data from #3. 
