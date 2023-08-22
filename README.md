# 🏗️ Circular Component Creator

The Build Systems Creator is a single-page web app developed with the Streamlit framework.

In this first version, it contains a building component creator with the following:
* Catalog section with a filter functionality to narrow down the search.
* Comparison section with properties like GWP/m² and U-Value. The user can put side-by-side the building components from the catalog.
* Creator section where the users can create their own components, adding layers, changing the material and its thickness.
* In the final section the users can compare their creations to the components available on the database.


## How to install and run the Streamlit App

The web app has been developed with Streamlit, a Python framework.
<details>
  <summary>Steps to access Streamlit on Windows</summary>
  
  * Install Git <kbd>https://git-scm.com/download/win</kbd>
  * Install Python <kbd>https://www.python.org/downloads/</kbd>
  * Install pip to manage python packages <kbd>https://pypi.org/project/pip/</kbd>
  * Open Command Prompt
  * Install pipenv to manage virtual environments `pip install pipenv`
  * Navigate to your "repos" folder with the command prompt using `cd`
    * To create a new folder use `mkdir`
    * To navigate back use `cd ..`
    * To see all the content in a directory use `dir`
  * Clone this repository `git clone https://github.com/BuildsystemsX/build-creator.git`
  * Navigate to repository `cd build-creator`
  * Create a virtual environment `pipenv install`
  * Activate the virtual environment `pipenv shell`
  * Install dependencies `pipenv install -r requirements.txt`
  * Test Streamlit `streamlit hello`
  * Run Streamlit app `streamlit run Overview.py`
    * Maybe the file name will change, but it is the Python file in the root folder
   
  To access the app again after installation:
  * Navigate to the cloned repository using the Command Prompt
  * Access the virtual environment `pipenv shell`
  * Run Streamlit app `streamlit run Overview.py`
  </details>
  

## Section Heading

This is filler text, please replace this with text for this section.

## Further Reading

This is filler text, please replace this with an explanatory text about further relevant resources for this repo
- Resource 1
- Resource 2
- Resource 3
