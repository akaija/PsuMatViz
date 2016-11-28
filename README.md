#PsuMatVis

##Visualise PseudoMaterials in Blender with <b>one command!</b>  

![Alt text](PseudoMaterial_screenshot.png?raw=true "Blender Screenshot")

### Set-up:  
  `mkdir -b ~/venv`  
  `pyvenv ~/venv/psumatvis`  
  `source ~/venv/psumatvis`  
  `cd path/to/psumatvis/repo`  
  `pip install -r requirements.txt`  

### To run:  
  `source ~/venv/psumatvis`  
  `cd pseudo_material_visualisation`  
  `blender empty_scene.blend --background --python blender_script.py <uuid>`  
