# Data Quality Checker 2.0
This is a data quality checker that identifies null values, detects duplicates, and can perform schema validation if the user chooses to enable it.
<br/>
<br/>
Tools used to build the data quality checker are `Python` & `Django`.
<br/>
<br/>
Upload a CSV file to assess data quality. The system will report the number of null values, specifying the columns and rows where they occur. It will also identify duplicate rows and highlight which entries repeat an original record.
<br/>
<br/>
The main goal is to allow users without database or SQL knowledge to quickly assess the quality of their data. For instance, someone preparing files for ingestion doesn’t need coding experience. This enables professionals who prepare datasets to validate them before they enter the ETL pipeline.
<br/>
<br/>
Furthermore, data engineers often work with files prepared by professionals in other fields, and they’re frequently responsible for validating datasets that may contain issues that aren’t immediately obvious. If the person preparing the data can check for problems such as missing values, duplicate rows, or schema mismatches in advance, it helps reduce bottlenecks and streamlines the overall process.
<br/>
<br/>
In some cases, null values and duplicate rows are not actual issues but reflect the intended structure of the dataset. Even so, it’s important to explicitly validate and approve these characteristics to ensure the data can be processed with a high level of quality.
<br/>
<br/>
Ensuring high-quality data at the source supports smooth processing and transformation throughout the pipeline, in cases when data is prepared outside the data engineering team. When data is flawed or not properly prepared at the source, it can lead to confusion and issues further downstream.
<br/>
### Libraries
`pip install xlrd`
<br/>
### Project Description
The program supports uploading CSV, XLS, and XLSX files. 
<br/>
<br/>
For program to process input, these files should have their column names in the first row, which is often typical for these formats, and all subsequent rows should contain data.
<br/>
<br/>
After upload, user is asked to perform schema validation, which can be skipped, if such action is not needed.
<br/>
<br/>
For schema validation, the column names are automatically extracted from the uploaded file, and the user is prompted to select the expected data type column. Choosing data type is not required, allowing users to validate specific columns without needing to define data types for all of them.
<br/>
<br/>
After this step, the user is redirected to a page where the results are displayed. These include the number of null values per column, along with a separate page that shows detailed information about null entries—such as their index and corresponding column. The results also highlight any duplicate rows and provide the outcome of the schema validation.
<br/>
<br/>
User can download PDF of validation results, which will include all views from above.
<br/>
### Overview
1. Upload file
2. Perform schema validation - Can be skipped
3. Results with PDF download option
4. Null value detail page
<br/>

## 2.0 version
This version seeks further improvements:
1. Adding superuser
2. Login, register & logout of user
3. Adding tables & migrations (SQLite) for archive of PDF generations
4. Testing out email/Slack integration
5. Mobile responsivity
<br/>

## Upgraded version 
In upgraded version of data quality checker, login, registration & logout of user were added, with corresponding `User` model. Main reason for adding this logic was to enable user archive of processed files. This way, a 'library' of processed files result, that is resulting PDFs are available to user, with a deletion option (to be added).
<br/>
<br/>
Model which supports archive is `File_Data` with following configuration:
```
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_id')
    file_id = models.AutoField(primary_key=True)
    row_number= models.IntegerField(null = True)
    original_file_name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=UPLOADED)
    uploaded_at = models.DateTimeField(auto_now_add = True, null = True)
```
<br/>
