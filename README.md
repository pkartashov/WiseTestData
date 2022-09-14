# WiseTestData
Python app to generate test data for best coverage


## Testing problem #1 is effective test coverage (i.e. data in use case/feature) 

This Python app uses 3 step approach to obtain optimal test data permutations

### Step 1.
Randomized, yet realistic test data generation based on each field type. E.g. Address should eb valid one, person name should be from a list of real people names, etc.
This allows more uniform distribution of test input, removes bias of tester

### Step 2.
Mark dependencies between fields (i.e. which field influences behavior such as validation of of others). This allows to reorder fields by priority. The app uses well-know PageRank algorithm (original google search) to reorder fields by their priority

### Step 3.
Based on reordered test data matrix (after Step 2 is completed), the app runs "All pairs" permmutations and outputs the combinations

## Get started:

1. Download the package and make sure all dependencies (in include) are installed (use pip install <package_name> or other convenient method on your python IDE)
2. Open TestData.xlsx and 
  2.1.build your fields schema on Data worksheet: first row is your logical naming of your fields; second row represents data type - use from dropdown menus supported pre-defined ones (String and Number will just generate random alpha string or numeric accordingly)
  2.2 build field dependency matrix in 'ref' worksheet as following:
3. Save the file (you can also rename it)
4. Execute the app job using one of 2 methods:
  - from IDE by calling runer = WiseTestData ("api", 14, 'TestData.xlsx', True, False, False)
  - run the API local server by executing uvicorn api:app --port 8000 --reload, then send GET request (e.g. in a browser) as follows: http://127.0.0.1:8009/generate/True/rows/11/skipshuffle/False/skippairs/False?excel=TestData.xlsx
5. Once the job is down, open the TestData.xlsx to get 1) generated test data without permutations on 'generated' worksheet 2) all recommended permutations for actual testing on 'WiseTD' worksheet
If you use to execute it in API mode, you will also obtain permutations (aka WiseTD) as JSON output after the GET request complete

### Where it can be used?
- Heavy data testing including migration, ETL, etc
- Complex business logic which requires data-driven approach to cover various paths
- Production and pre-production testing where dynamic and various data sets needed, such as  Blue/Green, Canary, Feature-flag deployments, as well as business validation such as A/B split testing, UAT and design of experiments

