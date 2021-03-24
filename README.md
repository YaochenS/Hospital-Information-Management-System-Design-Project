# Hospital-Information-Management-System-Design-Project
Designed the hospital information management system for doctors to take care of COVID-19 patients.

Python is the language we use

Please run MySQL - U root - P in terminal first< init.sql

And then python DB.py Run (please change first) DB.py Connect port password in the program)

Different user identities can be selected to login in the login interface. For example, 165690143690109823 is the user name of the attending doctor in the mild, severe and critical areas, and the initial password of all users is 000000

We mainly use the default primary indexing, Because each ID is unique and the amount of data is low, it can also be queried quickly through the primary key index. At the same time, all our automatic operations (for example, when the doctor changes the patient's status to rehabilitation, discharge or death in the original full area, there will be an isolation area or other areas automatically, and the qualified patients will be transferred to the previous patient's location and matched with the corresponding nurses For example, when considering new patients, we will consider whether there are spare beds and nurses. They are all written in Python statements in the program, and there is no trigger operation involved.

