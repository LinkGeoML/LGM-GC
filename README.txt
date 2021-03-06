---------------------------------------------------------
Geocoding plugin is a plugin for QGIS classifying roads.
---------------------------------------------------------

*****
The default installation path for QGIS plugins,where the plugins folder should be installed is defined as follows:

example: C:\\Users\\{text_user}\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins

To test the plugin,simply paste the folder in the path above
In QGIS python terminal:
(default_path=QgsApplication.qgisSettingsDirPath() + "\python\plugins"  )

The plugin is tested on windows operating system
*****
The plugin is divided in two sections:
1. Model Training Section    
2. Model Running Section
*****
This is geocoding version 1.1
*****

***** Model Training *****
------
step 1
As regards model training, at first the user loads a csv file (Train Data button) that is used for training the algorithm.
------
step 2
Next, the user runs the features extraction step through the features extraction button.
An experiments folder is created,which it should be selected through the Experiments Path button,in order to proceed to the next steps.
------
step 3
After that, the user runs the algorithm selection button.
------
step 4
Then he sets a classifier from the drop down menu, in order to run the model selection button.
------
step 5
Last step in training section is the model training feature that is mandatory to complete the the training of the algorithm.The user runs the model training feature through the Model Training button.
------
As regards the training data button and experiment path button,  right click on these buttons shows a pop up selection (What's this) that explains to the user what these buttons are used for.

***** Model Running *****

Furthermore, after training the algorithm, there is the Model Running section.
------
step 1 
The first button in this section is the File to classify button.
Here the user defines the csv file that is needed to be classified.
The full path of the selected file is shown in the field next to that button.
------
step 2
Next step is the Model Deployment button where the final results are going to be exported in the file specified as experiment path file.
The user defines that file before executing Model Deployment. 
------
step 3
When the Model Deployment is executed, the user can press the Show Recommendation Results button, where the results are shown in the Results Table field,which is placed in the section beneath.
------
step 4
When the results are loaded in the results table, the user is able to select the most sufficient result selecting the appropriate checkbox.
When the user finishes selecting the appropriate results, then the Select button can be pressed and a new file is created, where the choices of the user are stored. User defines where the file is going to be saved.
------
step 5
The user can select the maximum result for each category by pressing Auto Select button.
------
step 6
Next step is the Load Classification Results button where each category (original,arcgis,nominatim) is loaded as a separate layer in QGIS.
Each road is displayed as a point of interest in a map. The user can define the appropriate CRS before the pois are loaded.Each layer is represented with a unique color and all the layers can be represented simultaneously, so that the user can have a visual depiction of the results.
------
step 7
Last step is the Load User Results button. If the user has chosen the right category for each road (step 4), these choices are loaded as a separate layer in QGIS.That layer loads with greater significance over the rest layers (is put on the top of the layers list)


Also, the user can right click on the desired road in results table, a pop up menu is raised with three functions available.

*Show current address categories in map.
The active map focuses on all three categories, so that the user can define which result is the best.
Note that each category is depicted with different symbol for better separation among them

*Go to User's Choice Road 
The layer is focused on that road.The poi is highlighted yellow.The user should first load the user results as a layer(step 7) and then use this feature.

*Go to maximum probability point
The active map layer focuses on the result with the maximum rate. The poi is highlighted yellow. No need to select any checkbox from the Results Table area. 

Furthermore, when clicking on a road (poi) for each layer, a table with information is shown.
 
Note that with right clicking on each button in Model Running section, a pop up selection appears (what's this) that explains to the user the use of each button.


For more information, see the PyQGIS Developer Cookbook at:
http://www.qgis.org/pyqgis-cookbook/index.html

(C) 2011-2018 GeoApt LLC - geoapt.com
