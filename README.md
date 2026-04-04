# Data Quality Checker
This is a data quality checker that identifies null values, detects duplicates, and can perform schema validation if the user chooses to enable it.
<br/>
<br/>
Tools used to build the data quality checker are `Python` & `Django`.
<br/>
<br/>
Upload a CSV file to assess data quality. The system will report the number of null values, specifying the columns and rows where they occur. It will also identify duplicate rows and highlight which entries repeat an original record.
<br/>
<br/>
The main goal is to allow users without database or SQL knowledge to quickly assess the quality of their data. For instance, someone preparing files for ingestion doesn’t need coding experience. This enables professionals who prepare datsets to validate them before they enter the ETL pipeline.
<br/>
<br/>
Furthermore, data engineers often work with files prepared by professionals in other fields, and they’re frequently responsible for validating datasets that may contain issues that aren’t immediately obvious. If the person preparing the data can check for problems such as missing values, duplicate rows, or schema mismatches in advance, it helps reduce bottlenecks and streamlines the overall process.
<br/>
<br/>
In some cases, null values and duplicate rows are not actual issues but reflect the intended structure of the dataset. Even so, it’s important to explicitly validate and approve these characteristics to ensure the data can be processed with a high level of quality.
<br/>
<br/>
Ensuring high-quality data at the source supports smooth processing and transformation throughout the pipeline, in cases when data is prepared outside the data engineering team. When data is flawed or not properly prepared at the source, it can lead to confusion and issues further downstream.