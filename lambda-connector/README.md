# API Gateway and Lambda-Honeycode connector code deployment guide

### Note: You need to create your HoneyCode workbook and tables before you can deploy the API's. Instructions to deploy the HoneyCode portion of the scoring tool can be found in `honeycode-tables/` in this repo

First, create an IAM role with permissions for `AWSLambdaBasicExecutionRole` and `AmazonHoneycodeReadOnlyAccess`
1. Navigate to the Roles page in the [IAM console](https://console.aws.amazon.com/iam)
2. Click the blue `Create role` button
3. Select `Lambda` as the use case for this role
4. Using the filter bar, search for and select the AWS-managed policies: `AWSLambdaBasicExecutionRole` and `AmazonHoneycodeReadOnlyAccess`
5. Optionally add tags and a description, and finish creating your `Lambda-Honeycode-Getter` IAM role


Next, deploy `DC-got-talent-preliminary-scores.py` and `DC-got-talent-final-scores.py` as Lambda functions and set up their API Gateway REST endpoints
1. Open the Functions page on the Lambda console.
2. Choose Create function.
3. Select `Author from scratch`
4. Under Basic information, enter the following:
    - For function name, enter `DC-got-talent-preliminary-scores` or `DC-got-talent-final-scores`, respectively
    - For Runtime, confirm that Python 3.8 is selected
5. Expand the option to `change default execution role`, select `use an existing role`, and select the `Lambda-Honeycode-Getter` role that you just created.
6. Click "Create function"
7. In the in-browser code editing window, double-click on `Lambda_function.py` to open it in the editor, and copy/post in the code from `DC-got-talent-final-scores.py` or `DC-got-talent-preliminary-scores` respectively.
8. Update lines 19 and 20 with your [HoneyCode workbook and table ID's](https://docs.aws.amazon.com/honeycode/latest/UserGuide/table-row-operations-arns-and-ids.html)
9. Click the `Deploy` button to update your live Lambda function
10. Once deployed, you can configure the API Gateway endpoint by clicking the `Add trigger` button in the Function overview 
11. If you don't already have an existing API Gateway, select `Create an API`
    - Choose a `REST API`
    - Select `Open` for security
    - Optionally, expand the `Additional Settings` to set your own API name
12. If you have already created a REST API Gateway, select it from the dropdown
    - Select `Open` for security
13. Click the orange `Add` button
14. Once added, click the API Gateway tile in your Function overview
15. Expand the details for your API Gateway trigger, and make note of your API endpoint to add into `static-scoreboard/js/index.js`
