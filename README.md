# ash_alert

This tool is small piece of software to solve the exercise from https://github.com/heikoklein/krisuvik2norway.

# Installation

1.Go to https://www.anaconda.com/distribution/#download-section, and download anaconda for Python 3.7 according to your operation system (Ubuntu 20.04 in this case). Please choose anaconda instead of miniconda. Otherwise some packages won't be there when running the tool and it will crash. 

2. Install anaconda with the downloaded executable file.

3. Download install_volcano_linux. This file will create a conda environment and will install the necessary python packages.

4. Open a shell window, change directory to the location of the “install_volcano_linux” and on the command line
  write: $bash install_jupyter_linux

# Run the tool

In "src" folder, a file named "run_model.sh" is the file to start the process. It's only necessary to change the paths to "add_volcanos.sh" and "ash_alert.py".
All files in "src" folder must saved in the same directory, except "run_model.sh" after modifying paths. This also includes the folder "ne_10m_admin_0_sovereignty".

"run_model.sh" will execute another bash file to start the forecasting model. If succesful, this python tool will be executed afterwards.

The steps in this python  tool are:
1. Fetch the files in https://thredds.met.no/thredds/catalog/metusers/heikok/ash/krisuvik/catalog.html , select the newest (which corresponds to the last forecasting), and retieves it in the memory.
2. The second step is removing unnecessary variables, and applying a mask to filter Norwegian territory (only land). A shapefile is used for it.
3. If alert is raised, two output types will be created for the selected timestamp; a csv file and a map. Afterwards, all outputs will be gathered into a zip file.
4. If alert was raised, it will send an email from a sender address to receivers addresses. This must be set before running the tool. So, go to "send_email.py" to set email addresses. More info inside the script. This script was tested with a Gmail account as sender. You'll need to let third parties access to your gmail. This can cause a security leak, be aware.

Inside the scripts there is more info. But the two python scripts to modify variables are ash_alert.py and send_email.py

# Ideas for enhancement

Since I did not have acces to "add_volcanos.sh" I couldn't implement the following ideas:
1. Directly run the python tool from inside "add_volcanos.sh".
2. In "run_model.sh", I was forced to use the operator "&&" instead of "|". With "|" we could pass an output from "add_volcanos.sh" to the python tool. So, we
don't need to fetch over a webpage to select the latest forecast file.
3. I need to double check, but some opendap links in the catalog work well some others did not. Hence I developed 2 ways of accessing the data, see read_html.py.
Perhaps, you also want to double check those links.

The tool does the job, hopefully I did not leave any bug, but there is still room for optimisation. Due to time constraint I couldn't do the following:
1. Improve the map. Especially the projection. The projection the tool is using it is not optimal for high latitudes.
2. Improve the robustness of the code with assertations, time performance, etc.
3. Create other outputs, such as a different map, or even create a shapefile with the areas over the ash threshold.

This was a very complete exercise in my opinion. A bit short of time though, since I also need to attend my duties at my current position. I'll be glad if the code can be useful for Met Norway. Please, feel free to get in touch for any question.





