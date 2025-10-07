# Bookr Project Setup Guide

## 🔐 Security Setup

This project now uses environment variables to keep sensitive information secure.

### Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Generate a new SECRET_KEY for production:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Update `.env` with your values:**
   - Replace `SECRET_KEY` with the generated key
   - Set `DEBUG=False` for production
   - Update `ALLOWED_HOSTS` with your domain

### Important Security Notes

- ⚠️ **Never commit `.env` to version control** (it's already in .gitignore)
- ✅ **Always use `.env.example`** as a template for other developers
- 🔒 **Generate a new SECRET_KEY** for production environments
- 🚫 **Set DEBUG=False** in production

---

## 🐍 Virtual Environment Setup

### Automated Setup (Recommended)

Run the setup script:
```bash
./setup_venv.sh
```

### Manual Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

### Deactivate Virtual Environment

```bash
deactivate
```

---

## 📦 Dependencies

See `requirements.txt` for all project dependencies. Key packages:
- **Django 5.2.5+** - Web framework
- **python-decouple** - Environment variable management

---

## 🚀 Running the Project

### Development
```bash
# Activate virtual environment
source venv/bin/activate

# Run server
python manage.py runserver

# Access at: http://127.0.0.1:8000/
```

### Production Checklist
- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate new `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS` with production domain
- [ ] Use proper database (PostgreSQL)
- [ ] Set up static files serving
- [ ] Use a production server (gunicorn, uwsgi)
- [ ] Enable HTTPS
- [ ] Set up proper logging

---

## 📁 Project Structure

```
bookr/
├── venv/                  # Virtual environment (not in git)
├── mysite/                # Django project settings
├── reviews/               # Main app
├── .env                   # Environment variables (not in git)
├── .env.example           # Template for environment variables
├── requirements.txt       # Python dependencies
├── setup_venv.sh          # Setup script
├── manage.py              # Django management script
└── db.sqlite3            # Database (not in git)
```

---

## 🛠️ Troubleshooting

### Import Error: No module named 'decouple'
```bash
pip install python-decouple
```

### Permission Denied on setup_venv.sh
```bash
chmod +x setup_venv.sh
```

### Virtual Environment Not Activating
Make sure you're running:
```bash
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```
