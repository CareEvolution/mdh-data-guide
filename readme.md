# MyDataHelps Data Guide

This repository contains a set of tutorials and reference examples to help analysts and data scientists learn how to use the MyDataHelps Export Database to analyze data collected by a [MyDataHelps](https://careevolution.com/mydatahelps/) project.

The MyDataHelps Export Database is a hosted data store that is managed by CareEvolution and provides access to all data that has been exported from a MyDataHelps project. Learn more about what the Export Database is, and how it can provide access to your data assets with this summary and video introduction in the [MyDataHelps User Guide](https://support.mydatahelps.org/hc/en-us/community/posts/11970410819603-MyDataHelps-Export-Database-Overview). 

This repository is organized into two main sections:

### Example Notebooks

Try out the example [notebooks](https://github.com/CareEvolution/mdh-data-guide/blob/main/notebooks) to interpret and model your MyDataHelps data using Python and Pandas.

### Example Queries

Try out the example [queries](https://github.com/CareEvolution/mdh-data-guide/blob/main/queries) to explore and transform your MyDataHelps data using SQL. To run these queries, sign into [MyDataHelps Designer](https://designer.mydatahelps.org) and navigate to the Export Explorer page (under Settings for your project).

# Getting Started with Example Notebooks

1. Clone this repository.
2. Install [Python](https://www.python.org/downloads/) (if you do not already have Python 3.9 or later).
3. There are several environments to run Jupyter notebooks. If you do not already have a preferred solution set up, you can run the following command to install Jupyter Lab. Learn more about Jupyter notebooks and installation options at [jupyter.org](https://jupyter.org/install):

```
pip install jupyterlab
```

Once installed, run the following command to start Jupyter Lab:

```
jupyter lab
```

4. Gather Your Export Database Configuration Settings and Credentials

To obtain the configuration settings for your project's Export Database, open [MyDataHelps Designer](https://designer.mydatahelps.org) and navigate to the Settings tab for your project. Click Export Explorer. The External Applications tab will provide the required configuration settings that will be used in the example notebooks.

Each notebook has a cell that should be updated with the settings that you obtain for your project. 

Follow the instructions on the External Applications tab to place your credentials in your local [AWS credentials file](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html). This process ensures your credentials will never be saved in files that are managed by this repository. 