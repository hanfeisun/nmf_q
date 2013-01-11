from setuptools import setup, find_packages
setup( name="nmf_q",
       version="0.10",
       author="hanfei sun",
       license="LGPL",
       scripts=["./nmfQ.py","./nmfRec.py"],
       packages= find_packages())
