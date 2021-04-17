# terraform-analysis
The original Terraform network config files are located in folder 03-instance-with-multiple-network

The Python files are used to extract the resource and ACL information from the Terraform documents. It will also create the Graphviz diagram to visualize the resultant network.


Finally, The main.cpp file is the setup file which uses the configLego library to model the network as extacted. The config files needed by this are located in the terra folder. 
