import os
import shutil

# print(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

destination = os.path.join(os.path.dirname(os.path.abspath(__file__)),'suspect_images')
Base_dir = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'media')

# print(os.listdir(Base_dir))
for i in os.listdir(Base_dir):
    if i.endswith("png") or i.endswith("jpg") or i.endswith("jpeg"):
        try:
            os.mkdir(os.path.join(destination, i.split('_')[0]))
        except:
            pass
        shutil.move(os.path.join(Base_dir, i), os.path.join(destination, i.split('_')[0]))