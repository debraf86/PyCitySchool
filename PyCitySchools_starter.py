#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[20]:


# Get the values for the District Summary
numStudents = school_data_complete['Student ID'].nunique()
numSchools = school_data_complete['school_name'].nunique()
totalBudget = school_data['budget'].sum()

math_ave= school_data_complete['math_score'].mean()
reading_ave = school_data_complete['reading_score'].mean()
passing_rate = (math_ave+reading_ave)/2

# Passing grades are 70 and above
totalPassMath = school_data_complete.loc[school_data_complete['math_score'] >= 70,['math_score']].count()
percentMathPass = totalPassMath/numStudents*100
totalPassReading = school_data_complete.loc[school_data_complete['reading_score'] >= 70,['reading_score']].count()
percentReadingPass = (totalPassReading/numStudents)*100

# Create the district summary table
districtSummary = pd.DataFrame({
    'School Count': numSchools, 
    'Student Count': numStudents, 
    'Total Budget':totalBudget, 
    'Average Math Score':math_ave, 
    'Average Reading Score': reading_ave, 
    '% Passing Math':percentMathPass, 
    '% Passing Reading': percentReadingPass, 
    'Overall Passing Rate':passing_rate})

# display the district summary table
districtSummary


# In[30]:


# Get the values for the School Summary
schools = school_data_complete
schoolsOnly = school_data

schoolCount = schools['school_name'].value_counts()

groupedSchools = schools.groupby('school_name')
schoolBudget = groupedSchools['budget'].unique()

perStudentBudget = schoolBudget/schoolCount


schoolType = groupedSchools["type"].unique()
schoolAveMath = groupedSchools['math_score'].mean()
schoolAveReading = groupedSchools['reading_score'].mean()

# Passing grades are 70 and above
schoolPassMath = schools.loc[schools['math_score'] >= 70] 
schoolPassReading = schools.loc[schools['reading_score'] >= 70] 
schoolPassMathGrp = schoolPassMath.groupby(['school_name']).count()
schoolPassReadingGrp = schoolPassReading.groupby(['school_name']).count()
mathPercentPass = (schoolPassMathGrp['math_score']/schoolCount)*100
readingPercentPass = (schoolPassReadingGrp['reading_score']/schoolCount)*100
overallPassingRate = (mathPercentPass+readingPercentPass) /2
       
# create the school summary table
schoolSummary = pd.DataFrame({
    "Student Count":schoolCount,
    "School Type": schoolType, 
    "School Budget": schoolBudget, 
    "Per Student Budget": perStudentBudget,
    "Ave Math Score": schoolAveMath, 
    "Ave Reading Score":schoolAveReading, 
    "% Passing Math":mathPercentPass, 
    "% Passing Reading":readingPercentPass,
    "Overall Passing Rate":overallPassingRate})

# Display the school summary
schoolSummary


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[4]:


# get and display the top 5 schools by overall passing rate
sortedSchoolBest = schoolSummary.sort_values("Overall Passing Rate", ascending=False)
sortedSchoolBest.head()


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[5]:


# get and display the bottom 5 schools by overall passing rate
sortedSchoolWorst = schoolSummary.sort_values("Overall Passing Rate", ascending=True)
sortedSchoolWorst.head()


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[6]:


# get the school grades grouped 
ninthGrade = school_data_complete.loc[school_data_complete['grade'] == "9th"]
tenthGrade = school_data_complete.loc[school_data_complete['grade'] == "10th"]
eleventhGrade = school_data_complete.loc[school_data_complete['grade'] == "11th"]
twelfthGrade = school_data_complete.loc[school_data_complete['grade'] == "12th"]

groupedSchools9th = ninthGrade.groupby(['school_name']).mean()
groupedSchools10th = tenthGrade.groupby(['school_name']).mean()
groupedSchools11th = ninthGrade.groupby(['school_name']).mean()
groupedSchools12th = tenthGrade.groupby(['school_name']).mean()

# create the data table of math averages by grade
mathScoresbyGrade = pd.DataFrame ({
    "9th":groupedSchools9th["math_score"],
    "10th": groupedSchools10th["math_score"],
    "11th": groupedSchools11th["math_score"],
    "12th": groupedSchools12th["math_score"]
})
# display the table showing the average math scores by grade
mathScoresbyGrade


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[7]:


readingScoressbyGrade = pd.DataFrame ({
    "9th":groupedSchools9th["reading_score"],
    "10th": groupedSchools10th["reading_score"],
    "11th": groupedSchools11th["reading_score"],
    "12th": groupedSchools12th["reading_score"]
})
#display the table displaying the reading scores by grade
readingScoressbyGrade


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[34]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

spending_df = schoolSummary[["Student Count", 
                             "Ave Math Score", 
                             "Ave Reading Score", 
                             "% Passing Math", 
                             "% Passing Reading", 
                             "Overall Passing Rate",
                             "Per Student Budget"]]

spending_df["Spending Ranges(per student)"] = pd.cut(spending_df["Per Student Budget"], spending_bins, labels=group_names)
spending_df = spending_df.groupby("Spending Ranges(per student)")
spending_df.max()


# #Scores by School Size

# * Perform the same operations as above, based on school size.

# In[10]:


# Create bins to sort by school size
size_bins = [0, 1000, 2000, 5000]
group_titles = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

bySchoolSize = schoolSummary[["Student Count", "Ave Math Score", "Ave Reading Score", "% Passing Math", "% Passing Reading", "Overall Passing Rate"]]

bySchoolSize["School Size"] = pd.cut(bySchoolSize["Student Count"], size_bins, labels=group_titles)
bySchoolSize = bySchoolSize.groupby("School Size")
bySchoolSize.max()


# ## Scores by school type

# * Perform the same operations as above, based on school type.

# In[35]:


# Group scores by school type (district or charter)
# get the data for the scores by school type table
schoolCount2 = schools['type'].value_counts()
groupedByType =schools.groupby(['type'])
mathScoreByType = groupedByType ['math_score'].mean()
readingScoreByType = groupedByType ['reading_score'].mean()
passMathByType = schools.loc[schools['math_score'] >= 70] 
passReadingByType = schools.loc[schools['reading_score'] >= 70]
passMathByTypeGrp = passMathByType.groupby(['type']).count()
passReadingByTypeGrp = passReadingByType.groupby(['type']).count()
mathPercentPassByType = (passMathByTypeGrp['math_score']/schoolCount2)*100
readingPercentPassByType = (passReadingByTypeGrp['reading_score']/schoolCount2)*100
overallPassing = (mathPercentPassByType+readingPercentPassByType)/2

# Create the school type table
scoresBySchoolType = pd.DataFrame({
    "Average Math Score": mathScoreByType,
    "Average Reading Score": readingScoreByType,
    "% Passing Math":mathPercentPassByType,
    "% Passing Reading":readingPercentPassByType,
    "Overall Passing Rate": overallPassing
})

# Display the school type table grouped by school type (district or charter)
scoresBySchoolType


# In[ ]:




