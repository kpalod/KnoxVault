# KnoxVault Cloud Vault Application
Knoxvault is a secure and user-friendly cloud-based vault application that provides users with a two-factor authentication mechanism using facial recognition and password authentication. It allows users to register and set up their faces for authentication. Once logged in, users can perform various operations on their files, including viewing, modifying, downloading, and deleting. The application also tracks the time of the user's last access and last login.

## Features

:lock: **Two-Factor Authentication**: 
 - Users can authenticate themselves using facial recognition and password authentication, providing an extra layer of security.

:bust_in_silhouette: **User Registration and Face Setup**:
- Users can register and set up their faces for authentication within the application.

:closed_lock_with_key: **Secure Storage**:
- User photos are securely stored in an encrypted format using AWS S3, ensuring the privacy and security of user data.

🕵️ **Facial Matching**:
- The application utilizes the face_recognition library to match the user's facial features during login and grant access based on the authentication result.

:card_file_box: **Database Storage**:
- User information, including registration details, login history, and file metadata, is stored in an AWS RDS (PostgreSQL) database for efficient data management and retrieval.

:file_folder: **File Operations**:
- Once logged in, users can perform various operations on their files, such as viewing, modifying, downloading, and deleting.

:alarm_clock: **Last Access and Last Login Tracking**:
- The application tracks the time of the user's last access and last login, providing users with information about their account activity.

:rocket: **Deployment with AWS Elastic Beanstalk**:
- The application can be easily deployed and managed on AWS Elastic Beanstalk, ensuring scalability and high availability.

:globe_with_meridians: **Custom Domain and SSL/TLS Support**:
- The application can be mapped to a custom domain using AWS Certificate Manager and AWS Route 53, providing a secure and professional user experience.

## Technologies Used  

- **Flask**: Python web framework for building the application.

- **face_recognition**: A Python library for face detection and recognition.

- **AWS RDS** (PostgreSQL): Database service for storing user information.

- **AWS S3**: Object storage service for securely storing user photos.
 
- **AWS Boto3**: Python SDK for interacting with AWS services.

- **AWS Elastic Beanstalk**: Service for deploying and managing applications in the AWS cloud.

- **AWS Certificate Manager**: Service for managing SSL/TLS certificates.

- **AWS Route 53**: DNS web service for mapping the Beanstalk URL to a custom domain.


## How to run the Application locally 

1. Clone the repository:
   ```git clone https://github.com/kpalod/KnoxVault/tree/main```
2. Navigate to the directory and install all the required libraries

   ``` cd KnoxVault ```
   ``` pip install -r requirements.txt ```
   **NOTE** : You may have issues installing the facial_recognition library due to CMAKE issues, use linux instead of windows if possible or install the required tools using Microsoft Visual studio

3. Create a file named '.env' and add the following details to your file:
```
 DATABASE_URL='mysql+pymysql://##YOUR AWS RDS URL OR LOCAL DATABASE URL##/## DB NAME ##'
ACCESS_KEY_ID='## your access key for S3 bucket ##'
ACCESS_SECRET_KEY='## secret key for bucket ##'
BUCKET_NAME='## bucket name ##'

```

NOTE : If you dont want to use S3 bucket in your app yet, check the previous commits and you can find a version where S3 was not used yet. 

4. Run the application:
``` python application.py ```

