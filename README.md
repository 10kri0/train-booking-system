# 🚂 RailBook — Online Train Booking System

RailBook is a **full-stack train ticket booking web application** built using **Flask**.
It provides **two portals**:

* 👤 **User Portal** – search trains, book tickets, manage bookings
* 🛠 **Admin Portal** – manage trains, monitor bookings, and control the system

The system simulates a simplified **IRCTC-style railway reservation platform**.

---

# 🌟 Features

## 👤 User Features

* Secure **user registration & login**
* **Search trains** by source and destination
* **Real-time seat availability**
* **Ticket booking system**
* **Fare calculation**
* **Booking history**
* **Profile management**
* **Change password**

---

## 🛠 Admin Features

* Separate **admin authentication**
* **Add / edit / cancel / delete trains**
* **View and manage bookings**
* **User management**
* **Dashboard statistics**
* **Admin profile management**

---

## ⚙ General Features

* Responsive UI using **Bootstrap 5**
* Secure authentication with **Flask-Login**
* Password hashing using **Werkzeug**
* Custom **404 and 500 error pages**
* Automatic **database seeding**
* Docker support for containerized deployment

---

# 🛠 Tech Stack

| Component      | Technology                |
| -------------- | ------------------------- |
| Backend        | Python 3.11               |
| Framework      | Flask 3.x                 |
| ORM            | SQLAlchemy                |
| Database       | SQLite                    |
| Frontend       | HTML, CSS, JavaScript     |
| CSS Framework  | Bootstrap 5               |
| Authentication | Flask-Login               |
| Security       | Werkzeug password hashing |
| Environment    | python-dotenv             |
| Deployment     | Docker                    |

---

# 📋 Prerequisites

Make sure the following tools are installed:

* Python **3.11+**
* pip
* Git
* Docker *(optional)*

---

# 🚀 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/10kri0/train-booking-system.git
cd train-booking-system
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Copy the example file:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Edit `.env`:

```
SECRET_KEY=your-secret-key
DEBUG=True
```

---

## 5️⃣ Run the Application

```bash
python app.py
```

Open your browser:

```
http://localhost:5000
```

---

# 🔑 Default Admin Credentials

| Field    | Value                                                   |
| -------- | ------------------------------------------------------- |
| URL      | http://localhost:5000/admin/login                       |
| Email    | [admin@trainbooking.com](mailto:admin@trainbooking.com) |
| Password | Admin@123                                               |

⚠ Change the password after first login.

---

# 📁 Project Structure

```
train-booking-system
│
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
│
├── models/
│   ├── user.py
│   ├── admin.py
│   ├── train.py
│   ├── booking.py
│   └── station.py
│
├── routes/
│   ├── auth.py
│   ├── user.py
│   └── admin.py
│
├── templates/
│   ├── auth/
│   ├── user/
│   ├── admin/
│   └── errors/
│
├── static/
│   ├── css/
│   └── js/
│
└── Docs/
```

---

# 🗄 Database Tables

| Table    | Description              |
| -------- | ------------------------ |
| users    | Passenger accounts       |
| admins   | Administrator accounts   |
| trains   | Train schedule and seats |
| bookings | Booking records          |
| stations | Station master list      |

---

# 🔗 Main Routes

### Authentication

```
GET  /
GET  /login
POST /login
GET  /register
POST /register
GET  /logout
```

### User Routes

```
/user/dashboard
/user/search
/user/check-fare
/user/book/<train_id>
/user/booking-history
/user/profile
```

### Admin Routes

```
/admin/login
/admin/dashboard
/admin/trains
/admin/add-train
/admin/edit-train/<id>
/admin/bookings
/admin/users
```

---

# 🐳 Docker Deployment

Build image:

```bash
docker build -t railbook .
```

Run container:

```bash
docker run -p 5000:5000 railbook
```

Open:

```
http://localhost:5000
```

---

# 🔮 Future Enhancements

* Payment gateway integration
* Email notifications
* Mobile app support
* Multi-language support
* Advanced train search filters
* REST API support

---

# 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to your branch
5. Open a Pull Request

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Krish Patel**

GitHub:
https://github.com/10kri0

---

⭐ If you like this project, please **star the repository**.
