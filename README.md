# Open Exoplanet Catalogue 

## Execution
```
python exoplanet.py
```
*Optional Flags*
```
test_file=<filepath>    : Test using local file
debug=<True/False>      : Print # undefined occurrences
```
*Run against local test file*
```
python exoplanet.py   test_file=test_cases/case_1   debug=True
```
<br>

*Environment*
```
pip install requests
python version 3.6.13
```
<br>

## Test Cases

Case 1
```Result: passed ```
* Normal json file
* All values differ
* No "invalid" entries
<br>

Case 2
```Result: passed ```
* Multiple planets have a star with the same hottest temp
* grammar check
<br>

Case 3
```Result: passed. no output ```
* Empty json
<br>

Case 4
```Result: passed. debug flag shows correct count ```
* RadiusJpt is empty on some planets
<br>

Case 5
```Result: passed. placeholder "NoName" prints correctly ```
* Planet name is empty
<br>

Case 6
```Result: passed ```
* Varying number of planets discovered: 0, 1, 2
* grammar check
<br>

Case 7
```Result: passed ```
* 0 orphan planets
* grammar check
<br>

Case 8
```Result: passed ```
* 1 orphan planet
* grammar check
<br>

Case 9
```Result: passed ```
* 2 orphan planets
* grammar check
<br>

Case 10
```Result: passed ```
* 10 duplicates of the same planet
