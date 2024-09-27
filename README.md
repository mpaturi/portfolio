# Millie's Portfolio Projects https://mpaturi.github.io/portfolio/#

These are a few projects done my Millie as part of her Data Analysis journey. She has used various technologies and tools to showcase her skills. 
Click on the link (https://mpaturi.github.io/portfolio/#) to learn more about each of them.

1. ETL on Laptops dataset - With SQL and Power BI. This dataset was obtained from Kaggle which shows the different prices for laptops in Indian
   Rupees for laptops with myriad of configurations. The data was first cleaned with SQL to remove missing, duplicate data. Then the data elements
   were broken into different columns to make meaningful predictions. There is a step by step illustration of resultant data along with the SQL
   query in the pdf. Eventually after the ETL process, the data set was used in Power BI to extract meaningful insights in the form of dashboard
   visualizations. <br>
   Tools used - SQL Server, Power BI. <br>
   Data Source : https://www.kaggle.com/datasets/ehtishamsadiq/uncleaned-laptop-price-dataset <br>
   Data Pre Processing And ETL - https://mpaturi.github.io/portfolio/1ETL/SQL.pdf <br>

2. EDA on Titanic dataset - With Python. This data set was also obtained from Kaggle. This popular dataset was used to show the feature(s) which
   contributed towards predicting the Titanic passenger's survivability rate. After descriptive analysis, a in depth Univariate, Bivariate and
   Multivariate analysis on features is performed in this notebook. <br>
   Tools used - Python, Matplotlib, Seaborn. <br>
   Data Source : https://www.kaggle.com/datasets/shubhamgupta012/titanic-dataset <br>
   Python Notebook : [Titanic Notebook](https://github.com/mpaturi/portfolio/blob/010ac68a30eed9a70965f069561e3dc3e3c3231a/2Titanic/titanic.ipynb)

3. AWS, Flask Web App - With Plotly, Python. This dataset shows the US Flights with different carriers between different US cities for the first
   week of January 2023. This is only a smll part of the entire dataset. The goal of this project was to show case the ability to use AWS, Flask
   web app and show meaningful graphs with Plotly. User is encouraged to play around with Plotly graphs to get meaningful insights.<br>
   Data Source : https://www.kaggle.com/datasets/bordanova/2023-us-civil-flights-delay-meteo-and-aircraft?select=US_flights_2023.csv <br>
   Beanstalk Flask link : http://flightsfromlocal.us-east-2.elasticbeanstalk.com/

4. Excel with US Bikes dataset - This dataset again from Kaggle shows the Bike sales in US for the month of December, 2021. This includes the sales to countries
   outside of US also. The data was obtained in denormalized form with lot of repitition. Using Filter option of Excel, the data was first Normalized
   into different sheets. Then again it was Denormalized to bring meaningful columns into one sheet with much less repitition. XLOOKUP(), VBA script
   wsa used to make this possible. Once all the data was denormalized, then pivot tables were created to derive meaningful insights. And finally
   a dashboard was created to bring all the charts from each of the pivot tables was collected to show a meaningful story.
   Data Source : https://www.kaggle.com/code/stolltho/eda-hypothesis-testing-bike-sales/input?select=Sales.csv <br>
   Excel Data preprocessing, ETL, Visualization : https://mpaturi.github.io/portfolio/4BikesSales/BikeSalesDAWithExcel.pdf
