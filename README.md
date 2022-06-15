# ChinaCBEKnowledgeBase

## Repository structure
This repostitory contains all relevant files corresponding to the masters thesis around the China cross-border knowledge base. The contents are as follows:
* The file **FHNW_MT_Patrick_Mutzner_Artefact_CB-E-Commerce_China_Knowledge Base.pbix** represents the Power BI data set and dashboard containing the visualization of the work carried out.
* The folder [azfunc-mtcbefunctions](azfunc-mtcbefunctions) contains all files of the dynamic data collection function, and can be used to alter the code, and to create a new docker image.
* The folder [azcontainer-contents](azcontainer-contents) contains a representation of the container structure of an Azure storage account, including the storage blobs which can be uploaded once a new storage account is provisioned.
* The folder [postman-collection-example](postman-collection-example) contains an example collection of function calls which can be used as starting point or as a reference.

## Getting ready instructions for users (consuming what is currently here):

### Prepare the local environment (use case: no code manipulation planned)
1. Install [Postman](https://www.postman.com/downloads/) to have a convenient tool to run the API calls, and overwrite the default variables.
2. Install [Power BI Desktop](https://powerbi.microsoft.com/en-us/desktop/) to be able to open the Power BI file, and edit it if required. When no editing of the Power BI file is intended, it can also be uploaded to a Power BI workspace within your Microsoft tenant

## Getting ready instructions for developers (consuming and changing what is currently here, or completely fresh implementations):

### Prepare the local environment (use case: code manipulation planned)
1. Install [Visual Studio Code](https://code.visualstudio.com/download) or another preferred code editor. Used to edit the code of the dynamic data collection function, if needed.
2. Run through [this tutorial](https://code.visualstudio.com/docs/python/python-tutorial) to prepare Visual Studio Code for Python programming
3. Install the Docker extention for Visual Studio Code
4. Install [Postman](https://www.postman.com/downloads/) to have a convenient tool to run the API calls, and overwrite the default variables.
5. Install [Docker Desktop for your operating system](https://docs.docker.com/desktop/) to build and push the Docker image to the docker hub.
6. Install [Power BI Desktop](https://powerbi.microsoft.com/en-us/desktop/) to be able to open the Power BI file, and edit it if required. When no editing of the Power BI file is intended, it can also be uploaded to a Power BI workspace within your Microsoft tenant

### Prepare the Azure cloud environment (use case: Azure infrastructure is not existing anymore, or a re-build is planned for any other reason)
1. Run through the steps from the last section: Prepare the local environment (use case: code manipulation planned).
2. Within an Azure tenant of your liking, create a resource group with the name RESOURCEGROUPNAME.
3. In the Azure portal, navigate to Cognitive Services | Translator, and create a new translator instance within the resource group RESOURCEGROUPNAME with a name, the region and with pricing tier of your preference (free tier suffices). Allow all networks to access, and disable the system managed identity.
4. Once the translator instance has been deployed, make sure to note down the API key and the region (to be found under the menu item "Keys and Endpoint", there are needed later on.
5. For preparing the storage account to store the data for the Power BI to access (core data and outputs from the dynamic collection), run the following command against the Azure CLI: ```az storage account create --name STORAGEACCOUNTNAME --location AZUREREGIONNAME --resource-group RESOURCEGROUPNAME --sku Standard_LRS```.
6. Create the app service plan which will later be used from the function: ```az functionapp plan create --resource-group RESOURCEGROUPNAME --name APPSERVICEPLANNAME --location AZUREREGIONNAME --sku B1 --is-linux```.
7. Create the function app itself. Please note, that the docker image used need to be set to your own image residing in the docker hub. ```az functionapp create --name FUNCTIONAPPNAME --storage-account STORAGEACCOUNTNAME --resource-group RESOURCEGROUPNAME --plan APPSERVICEPLANNAME --deployment-container-image-name DOCKERHUBREPONAME/IMAGENAME:latest```.
8. Run the following command and copy the STORAGEACCOUNTCONNECTIONSTRING (output of the following command) somewhere to have it at hand for the next step: ```az storage account show-connection-string --resource-group RESOURCEGROUPNAME --name STORAGEACCOUNTNAME --query connectionString --output tsv```.
9. Configure the function app: ```az functionapp config appsettings set --name FUNCTIONAPPNAME --resource-group RESOURCEGROUPNAME --settings STORAGEACCOUNTCONNECTIONSTRING```.
10. Run the following command to get the CICDURL of the function app. This URL can be configered as webhook in the Docker Hub containing the Docker image, to update the function app automatically once a change on the image has been done. ```az functionapp deployment container config --enable-cd --query CI_CD_URL --output tsv --name FUNCTIONAPPNAME --resource-group RESOURCEGROUPNAME```.
11. In your Docker hub, at the respective image, set the CI/CD web hool to the copied CICDURL. If the repository or the image does not yet exist, please keep it in your head to set the value later. If you do not set it, you will have to re-deploy the Azure function after every single change of the code and therefore also the Docker image.
12. In Azure, navigate to your storage account STORAGEACCOUNTNAME, go to the menu item "Access Control (IAM)" and add the "Storage Account Backup Contributor" role assignment for your FUNCTIONAPPNAME.
13. In Azure, navigate to your storage account STORAGEACCOUNTNAME, and go to the menu item "Containers". For each folder in the [azcontainer-contents](azcontainer-contents) folder of this repository, create a container with the same name as the sub-folder (e.g. mtcbecoredata-categories-manual), and upload the blobs (files) from each folder to the respective container. You can set the "public access level" option of the containers to Private (no anonymous access).
14. Open your code editor, and navigate to the file [__init__.py](azfunc-mtcbefunctions\MTCBEFunction\__init__.py), and change lines 43 ``subscription_key = KEY_FROM_STEP_4```` and 49 ``location = LOCATION_FROM_STEP_4````.
15. Save the change, right-click [Dockerfile](azfunc-mtcbefunctions\Dockerfile) and select **Build Image**.
16. Run ```docker tag IMAGENAME DOCKERHUBREPONAME/IMAGENAME:latest``` to build the image, and then ```docker push DOCKERHUBREPONAME/IMAGENAME:latest``` to push it to the Docker Hub.
17. Wait some moments, and your code changes should be automatically applied to the function app in Azure, as long you did set the webhook for the repository to CICDURL.

You are now ready to run the function, and see the output of the CBE knowledge base dynamic data collection function. You can do so either directly in the Azure portal by navigating to your FUNCTIONAPPNAME -> Functions -> MTCBEFunction -> Get Function URL -> default (function key) -> copy and call it in the browser or by opening postman and importing the collection found at [MT CBE KB Dynamic Data Collection Funtion.postman_collection.json](postman-collection-example\MT CBE KB Dynamic Data Collection Funtion.postman_collection.json) (consider changing the function URL and function key found in the Azure portal). Using postman has the benefit that you can see examples of the function calls including the overwrite of the default parameters. Please consider, the function can run up to 5 minutes to collect all data.

## Possible issues and limitations
### No categories are returned for one or more platforms. This can have multiple reasons:
* The function has been called more than once a day or within a short period of time. This could trigger the anti-scraping mechanisms of some platforms. In this case, try again later.
* The HTML tags, classes or ID's used to identify the navigation items has been changed by one or more platforms. In this case, use the inspection mechanism of your browser to find the appropriate way to identify the respective HTML elements, and either update the default value configuration for the respective platform in [__init__.py](azfunc-mtcbefunctions\MTCBEFunction\__init__.py) or use Postman to pass the new values to the function call (this option is best to try it out until it runs properly).
* Any other issues, which should be identifiable by navigating to your FUNCTIONAPPNAME -> Functions -> MTCBEFunction -> Code + Test -> Monitor to consume the live log written at the time the function is called. Any errors generates from Python will be printed here. After the problem is found, do the necessary changes and push the image again to the Docker Hub.

### No monthly active user numbers are returned for one or more platforms. This can have multiple reasons:
* The function has been called more than once a day or within a short period of time. This could trigger the anti-scraping mechanisms of Google. In this case, try again later.
* The query used to get an answer box on top of the Google results is not generating (anymore) this answer box. If this is the case, adpt the query until Google "knows" the answer again and adopt either the default parameters or pass the changed query as parameter into the function call.
* Google did change the HTML tag containing the anwer box. Currently, the code looks for a bold text within a block-component element: ```//block-component//b```. Use the inspection mechanism of your browser to identify the new HTML element, and update line 34 in the file [__init__.py](azfunc-mtcbefunctions\MTCBEFunction\__init__.py), and create and and push the image again to the Docker Hub.

### A HTML 500 error is returned when calling the function. Also this can have multiple reasons. In general, it points towards an issue within the function itself.
* Narrow the issue down by navigating to your FUNCTIONAPPNAME -> Functions -> MTCBEFunction -> Code + Test -> Monitor to consume the live log written at the time the function is called. Any errors generates from Python will be printed here. After the problem is found, do the necessary changes and push the image again to the Docker Hub.
* When building the docker image, the newest version of Chromium browser is installed in the image. For the web scraping, Selenium needs the [ChromeDriver executeable](azfunc-mtcbefunctions\MTCBEFunction\chromedriver). Chromium only supports the last two versions of ChromeDriver. The solution for this problem is simple: download the [latest version of ChromeDriver](https://chromedriver.chromium.org/downloads), replace the file ChinaCBEKnowledgeBase\azfunc-mtcbefunctions\MTCBEFunction\chromedriver with the new one, build the docker image, push it to the Docker hub, and wait until the change is applied in the Azure function.

In case of issues, do not hesitate to contact me via GitHub
