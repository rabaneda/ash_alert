#!/bin/bash

#PLEASE MODIFY PATHS TO FOLDERS/FILES: ".conda", "add_volcano.sh", and "ash_alert.py"

source activate /home/USER/.conda/envs/volcano

# 00 meteo, 06 eruption
30 8 * * * ERUPT=06:00 /PATH/TO/FOLDER/add_volcanos.sh && python /PATH/TO/FILE/ash_alert.py

# 06 meteo, 12 eruption
30 14 * * * ERUPT=12:00 /PATH/TO/FOLDER/add_volcanos.sh && python /PATH/TO/FILE/ash_alert.py

# 12 meteo, 18 eruption
30 20 * * * ERUPT=18:00 /PATH/TO/FOLDER/add_volcanos.sh && python /PATH/TO/FILE/ash_alert.py

# 18 meteo, 00 eruption
30 2 * * * ERUPT=00:00 /PATH/TO/FOLDER/add_volcanos.sh && python /PATH/TO/FILE/ash_alert.py


