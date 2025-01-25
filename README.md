# LeaveApp - Backend

## Description

**LeaveApp** is a web-based leave application and approval system that allows employees to submit leave requests and managers to approve or reject them. The system provides functionalities like user authentication, leave status management, and a report on the total leave status.

The objective of this backend project is to implement a secure and efficient leave application system with role-based access control, including employee leave submission, manager approval, and leave status management.

## Features

- **User Authentication**: Secure login and registration system for employees and managers.
- **Leave Application Submission**: Employees can submit leave requests specifying leave type, duration, and reason.
- **Leave Approval Workflow**: Managers can review and approve or reject leave requests submitted by employees.
- **Leave Reports**: Generate reports showing the total leave taken by each employee, with detailed leave types and statuses.
- **Role-based Access**: Differentiates between employees and managers for specific functionalities.
- **CORS Support**: Configured to allow cross-origin requests, enabling the frontend to interact with the backend.

## Technologies Used

- **Backend Framework**: Django
- **Authentication**: JWT Authentication (djangorestframework-simplejwt)
- **Database**: PostgreSQL / MySQL (configurable)
- **Additional Libraries**: Django Rest Framework, Django Allauth, dj-rest-auth, and more
- **CORS**: django-cors-headers
- **Environment Management**: django-environ for managing environment variables

## Setup Instructions

### 1. Clone the repository:

Clone the backend repository to your local machine:

```bash
git clone <backend-repo-url>
cd LeaveApp-backend
