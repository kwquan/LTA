# LTA ELT
![alt text](https://github.com/kwquan/LTA/blob/main/process.png)
This project is an end-to-end ELT[Extract,Load,Transform] pipeline that does the following:
1) Calls the LTA API to get CrowdLevel for each station on the East-West line[https://datamall.lta.gov.sg/content/dam/datamall/datasets/LTA_DataMall_API_User_Guide.pdf]
2) Saves the data to volume as temp.tsv[under dags]
3) Creates stations table in PostgreSQL if it doesn't exists
4) Pushes temp.tsv to stations table
5) Checks if there are at least 30 minutes worth of records. If yes, print out stations whose CrowdLevel has changed in the past 30 minutes
