## Prerequisites

You'll need the following:
* [IBM Cloud account](https://console.ng.bluemix.net/registration/)
* [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)

## 1. Clone the sample app

Now you're ready to start working with the app. Clone the repo and change to the directory where the sample app is located.
  ```
git clone https://github.com/IBM-Cloud/get-started-python
cd get-started-python
  ```

  Peruse the files in the *get-started-python* directory to familiarize yourself with the contents.

## 2. Run the app locally

**********************************************************************************************************************************
Imortant note:
If you're going to run the app locally, change the app run code from:
app.run(host='0.0.0.0', port=int(port))
To
app.run(host='127.0.0.1', port=int(port))
**********************************************************************************************************************************

  ```
pip install -r requirements.txt
  ```

Run the app.
  ```
python server.py
  ```

 View your app at: http://localhost:10000

## 3. Prepare the app for deployment

To deploy to IBM Cloud, it can be helpful to set up a manifest.yml file. One is provided for you with the sample. Take a moment to look at it.

The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. In this manifest.yml **random-route: true** generates a random route for your app to prevent your route from colliding with others.  You can replace **random-route: true** with **host: myChosenHostName**.
 ```
 applications:
 - name: <you app name in the cloud>
   random-route: true
   memory: 256M
 ```

## 4. Deploy the app

You can use the Cloud Foundry CLI to deploy apps.

Choose your API endpoint
   ```
cf api <API-endpoint>
   ```

Replace the *API-endpoint* in the command with an API endpoint from the following list.

|URL                             |Region          |
|:-------------------------------|:---------------|
| https://api.ng.bluemix.net     | US South       |
| https://api.eu-de.bluemix.net  | Germany        |
| https://api.eu-gb.bluemix.net  | United Kingdom |
| https://api.au-syd.bluemix.net | Sydney         |

Login to your IBM Cloud account

  ```
cf login
  ```
Enter your email ID and password.


Push the app
  ```
bluemix app push <your app name>
  ```

This can take a minute. If there is an error in the deployment process you can use the command `cf logs <your app name> --recent` to troubleshoot.

When deployment completes you should see a message indicating that your app is running.  View your app at the URL listed in the output of the push command.

**********************************************************************************************************************************
Important Note:
This app needs a database connected to it in order to work and fetch data. The dataset used here is earthquake data which you can get it as a CSV file from the following URL:
https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php

Also, befor uploading the CSV file to the cloud's DB2, you have to change the time date format in the Excel sheet using to Excel build-in functions:
Firstly, apply this function to the time column:
  =SUBSTITUTE(A55,"Z","+00:00")
  
Then, apply this function to the result of the previus step.
  =--SUBSTITUTE(LEFT(B3,FIND("+",B3)-1),"T"," ")
**********************************************************************************************************************************
