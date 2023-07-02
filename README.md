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


