# scaffold-pathway-maker

The scaffold pathway maker is a Python script which takes as inputs an OpenCMISS-ZINC Ex whole-body scaffold and a JSON 
connectivity information and outputs OpenCMISS-ZINC Ex neuronal path embedded within the 3D whole body. This script 
works by first discovering the edges that make up a neuronal path from the JSON file, matching those edges to the
 corresponding fiducial markers in the whole body scaffold, and then generating a 3D nerve pathway within the body.