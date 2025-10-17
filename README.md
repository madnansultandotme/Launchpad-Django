# 🚀 LaunchPad

> **A multi-tenant, open-source CMS built with Django - where every user gets their own website instantly.**

LaunchPad lets users **create and manage their own mini-websites** under unique subdomains — just like `launchpad.dev/username/`.  
Each user gets their own dashboard, pages, and theme — built on Django’s powerful and extensible architecture.

---

## Overview

**LaunchPad** is designed to showcase the full potential of **Django’s multi-tenancy**  a single platform serving multiple independent sites.

Think of it as an open-source foundation for platforms like **Hashnode**, **Notion Sites**, or **Substack**, built entirely in Django.

---

## Features

### Core Features
- **Multi-Tenant System** – Each user gets a dedicated site and dashboard.
- **Page Management** – Create, edit, and publish static pages.
- **Themes & Templates** – Choose between built-in visual styles.
- **Dashboard** – Manage content, settings, and customization.
- **Public Rendering** – Live site accessible via `/username/` routes.
- **User Authentication** – Secure sign-up and login flow.
- **Extensible Architecture** – Add more modules like Blog, Gallery, or Contact forms later.

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Django |
| Database | PostgreSQL | SQlite |
| API | Django REST Framework (future) |
| Auth | Django AllAuth |
| Frontend | Django Templates + Tailwind CSS |
| Styling | Tailwind CSS |

---


## Getting Started

Follow the steps below to set up **LaunchPad** on your local machine 👇

### 1️⃣ Fork the Repository
Click the **Fork** button (top-right) on this repository to create your own copy.

---

### 2️⃣ Clone Your Fork
```bash
git clone https://github.com/<your-username>/launchpad.git
cd launchpad
```
### 3️⃣ Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
### 4️⃣ Install Dependencies
Make sure you have pip updated:

```bash
pip install --upgrade pip
```
Then install all required packages:
```bash
pip install -r requirements.txt
```
Also install the following 
pip install django-allauth
pip install django-tailwind
pip install django-tailwind[reload]

### 5️⃣ Apply Migrations

Run the following commands to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```
### 6️⃣ Create a Superuser (Optional)
To access the Django admin panel:

```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 7️⃣ Run the Development Server
Start the local Django server:

```bash
python manage.py runserver
```
Now open your browser and go to:
```bash
http://127.0.0.1:8000/
```
You should see the LaunchPad home page 🎉

### ✅ You're All Set!
You now have LaunchPad running locally and ready to explore, customize, or contribute!

### Modification Guide
If you start changing files and you run seperate terminal for tailwind css by the following command
```bash
python manage.py tailwind start
```
and you encounter error NPM not found. Go to settings.py and change following with your npm path.
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

### Modification Guide
If you start modifying files and run a separate terminal for Tailwind CSS using the following command:
```bash
python manage.py tailwind start
```
and you encounter an “NPM not found” error, go to your settings.py file and update the following line with your NPM path:
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"