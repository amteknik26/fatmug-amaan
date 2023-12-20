## Fatmug Assignment - Amaan
In this README file I will provide you with everything you need to evaluate my assignment.

*In case of any discrepancies please feel free to mail me at : amaan5800@gmail.com or DM me via LinkedIn*

&nbsp;
&nbsp;
## Setup
1. Download the repo as .zip file, extract it and open the folder in an editor
2. Create virtual environment:
```bash
  python -m venv .venv
```
3. Activate virtual environment
```bash
  . .venv/Scripts/activate
```
4. Install dependencies
```bash
  pip install -r requirements.txt
```
5. Run migrations using the below two commands
```bash
    python manage.py makemigrations fatmug_main
    python manage.py migrate 
```
6. Start the server using 
```bash
  python ./manage.py runserver
```
&nbsp;
## End User Flow
The typical flow would be like
1. Create Vendor
2. Create a PurchaseOrder for said vendor 
3. Hit acknowledge endoint to acknowledge the PurchaseOrder
4. Update the PurchaseOrder status to 'completed'
5. Trigger metrics calculation

&nbsp;
## Run test suite
Tests are located inside 'tests' directory of 'fatmug_main' app. When inside the project you can run the below
command to execute all the test cases for views, urls and models.
```bash
  python manage.py test fatmug_main.tests.test_urls fatmug_main.tests.test_models fatmug_main.tests.test_views
```
There are 15 test cases which must return OK

&nbsp;
## API Documentation
The views have been extensively documented using 'docstrings. Additionally I have used swagger to document the APIs.
Once the server is up and running, You can visit http://127.0.0.1:8000/swagger/ to check out the documentaion

&nbsp;
## Obtain Token 
To obtain authentication token, You must create a superuser and then generate a token using that user
1. Create superuser. Give desired username and password
```bash
  python manage.py createsuperusers
```
2. Generate token. Pass the username generated in the previous step.
```bash
  python manage.py drf_create_token <username>
```
3. The token will be printed on the console. Save it in a textfile. Because we need to pass this token
in the 'Authorization' header to be able to hit the API endpoints. You can use my public [Postman](https://www.postman.com/descent-module-cosmologist-24341852/workspace/fatmug-amaan/collection/20327661-7bca455c-c2c2-4da8-9d47-e2420c251a0f?action=share&creator=20327661) collection
to hit my endpoints

&nbsp;
## Test Endpoints
You can test my endpoints by using my public [Postman](https://www.postman.com/descent-module-cosmologist-24341852/workspace/fatmug-amaan/collection/20327661-7bca455c-c2c2-4da8-9d47-e2420c251a0f?action=share&creator=20327661) collection 


