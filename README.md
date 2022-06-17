# Eniac-WBS
Data cleaning and representation

It is a training project done withing a Data Science Boot Camp at the WBS Coding School https://www.wbscodingschool.com/
This project was devoted to exploration, cleaning and representation of data of a dummy company called Eniac. The aim of this analysis was to find dependencies between the discounts which the company proposes and the revenue.

Data came in four CSV tables which were analysed using **Pandas** python library.
Initial exploration revialed many duplicated rows and Nan values which were exluded in the cleaning step. Data types were recovered when possible (dates were converted from strings to datetime format, prices initialy presented as strings with several dodts were converted to float). Rows which were not connected with other tables were excluded. Extreme outlaers were found and droped.

Data presentation was done using **Matplotlib** and **Seaborn** python libraries. General positive correlation between discounts and revenue as well as influence of special dates was revialed. 
