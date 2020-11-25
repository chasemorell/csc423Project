import cx_Oracle
import pandas as pd

"""
Some quick start guides:
* cx_Oracle 8: https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
* pandas: https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
"""
# TODO change path of Oracle Instant Client to yours

cx_Oracle.init_oracle_client(lib_dir = "/Users/chasemorell/instantclient_19_8")

dsnStr = cx_Oracle.makedsn("lawtech.law.miami.edu", "1521", "CSC423")

# TODO change credentials
# Connect as user "user" with password "mypass" to the "CSC423" service
# running on lawtech.law.miami.edu
connection = cx_Oracle.connect(
   user = "CHMOCSC423", password = "morell0521", dsn=dsnStr)

def query(q):
	print("**** Query Results ****")
	cursor = connection.cursor()
	cursor.execute(q)

	# get column names from cursor
	columns = [c[0] for c in cursor.description]
	# fetch data
	data = cursor.fetchall()
	# bring data into a pandas dataframe for easy data transformation
	df = pd.DataFrame(data, columns = columns)
	print(df) # examine
	print(df.columns)
	print("\n");
	# print(df['FIRST_NAME']) # example to extract a column


#Get the tutors who have classes that have an enrollment greater than 1
query("""
SELECT * 
FROM TUTOR
WHERE TUTORID IN (SELECT TUTORID 
                FROM COURSE
                WHERE CURRENTENROLLMENT > 1)
""");

#List the enrollment details
query("""
    SELECT *
    FROM ENROLLMENT
    """);

#Get the courses that are longer than 20 weeks
query("""
    SELECT *
    FROM COURSEDETAILS
    WHERE WEEKS > 20
    """);
#Get the students enrolled in all the Spanish 1 classes
query("""
SELECT * 
FROM STUDENT
WHERE STUDENTID IN (SELECT STUDENTID FROM ENROLLMENT WHERE COURSEID IN (SELECT COURSEID FROM COURSE WHERE COURSENAME = 'Spanish 1'))
""");

#Get the classes that are currently in session (being offered)
query("""
SELECT * 
FROM COURSE c
WHERE TRUNC(ADD_MONTHS(STARTDATE, (SELECT WEEKS FROM COURSEDETAILS d WHERE c.COURSENAME = d.COURSENAME))) >  CAST(SYSDATE as DATE) 
AND STARTDATE < SYSDATE
""");

#Get the student info of students that have not payed the fees
query("""
SELECT * 
FROM STUDENT s
WHERE STUDENTID IN (SELECT STUDENTID
FROM ENROLLMENT
WHERE FEEPAYED = 'no');
""")