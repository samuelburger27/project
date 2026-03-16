# About Dataset
This data approach student achievement in secondary education of two Portuguese schools. The data attributes include student grades, demographic, social and school related features) and it was collected by using school reports and questionnaires. Two datasets are provided regarding the performance in two distinct subjects: Mathematics (mat) and Portuguese language (por). 

## Source
Paulo Cortez, University of Minho, GuimarÃ£es, Portugal, http://www3.dsi.uminho.pt/pcortez

# Attributes
## Attributes for both Math and Portuguese language course datasets
1 id - unique record id matching one student (numeric)
2 school - student's school (binary: "GP" - Gabriel Pereira or "MS" - Mousinho da Silveira)
3 sex - student's sex (binary: "F" - female or "M" - male)
4 age - student's age (numeric: from 15 to 22)
5 address - student's home address type (binary: "U" - urban or "R" - rural)
6 famsize - family size (binary: "LE3" - less or equal to 3 or "GT3" - greater than 3)
7 Pstatus - parent's cohabitation status (binary: "T" - living together or "A" - apart)
8 Medu - mother's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)
9 Fedu - father's education (numeric: 0 - none,  1 - primary education (4th grade), 2 – 5th to 9th grade, 3 – secondary education or 4 – higher education)
10 Mjob - mother's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
11 Fjob - father's job (nominal: "teacher", "health" care related, civil "services" (e.g. administrative or police), "at_home" or "other")
12 reason - reason to choose this school (nominal: close to "home", school "reputation", "course" preference or "other")
13 guardian - student's guardian (nominal: "mother", "father" or "other")
14 traveltime - home to school travel time (numeric: 1 - <15 min., 2 - 15 to 30 min., 3 - 30 min. to 1 hour, or 4 - >1 hour)
15 studytime - weekly study time (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)
16 failures - number of past class failures (numeric: n if 1<=n<3, else 4)
17 schoolsup - extra educational support (binary: yes or no)
18 famsup - family educational support (binary: yes or no)
19 paid - extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)
20 activities - extra-curricular activities (binary: yes or no)
21 nursery - attended nursery school (binary: yes or no)
22 higher - wants to take higher education (binary: yes or no)
23 internet - Internet access at home (binary: yes or no)
24 romantic - with a romantic relationship (binary: yes or no)
26 famrel - quality of family relationships (numeric: from 1 - very bad to 5 - excellent)
26 freetime - free time after school (numeric: from 1 - very low to 5 - very high)
27 goout - going out with friends (numeric: from 1 - very low to 5 - very high)
28 Dalc - workday alcohol consumption (numeric: from 1 - very low to 5 - very high)
29 Walc - weekend alcohol consumption (numeric: from 1 - very low to 5 - very high)
30 health - current health status (numeric: from 1 - very bad to 5 - very good)
31 absences - number of school absences (numeric: from 0 to 93)

## Grades (targets)
these grades are related with the course subject, Math or Portuguese:
33 G1 - first period grade (numeric: from 0 to 20)
33 G2 - second period grade (numeric: from 0 to 20)
34 G3 - final grade (numeric: from 0 to 20, output target)

