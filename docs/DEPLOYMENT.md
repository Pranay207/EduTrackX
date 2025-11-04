# EduTrackX Deployment Guide

## Deployment Options

### 1. Replit Deployment (Recommended for Quick Start)

EduTrackX is pre-configured for Replit deployment.

**Steps:**
1. Click the "Publish" button in Replit
2. Choose deployment type: "Autoscale" for web apps
3. Configure domain (optional)
4. Click "Deploy"

Your app will be live with a Replit domain!

### 2. Manual Production Deployment

#### Prerequisites
- Server with Python 3.11+ and Node.js 20+
- Domain name (optional)
- SSL certificate (recommended)

#### Backend Deployment

**Using Gunicorn (Recommended):**
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5001 run:app --access-logfile - --error-logfile -
```

**Production Environment Variables:**
Create `.env.production`:
```
JWT_SECRET_KEY=your-very-secure-secret-key-change-this
FLASK_ENV=production
PORT=5001
```

#### Frontend Deployment

**Build for Production:**
```bash
cd frontend
npm run build
```

This creates an optimized production build in `frontend/dist/`.

**Serve with Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 3. Docker Deployment

**Dockerfile (Backend):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tesseract-ocr

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "run:app"]
```

**Dockerfile (Frontend):**
```dockerfile
FROM node:20-alpine as builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5001:5001"
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

### 4. Cloud Platform Deployment

#### Heroku

**Backend:**
1. Create `Procfile`:
```
web: gunicorn -w 4 run:app
```

2. Deploy:
```bash
heroku create edutrackx-api
git subtree push --prefix backend heroku main
```

#### Vercel (Frontend)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
cd frontend
vercel --prod
```

#### AWS EC2

1. Launch Ubuntu instance
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip nodejs npm tesseract-ocr nginx
```

3. Clone repository and setup
4. Configure Nginx as reverse proxy
5. Use PM2 or systemd for process management

### 5. Database Migration (Production)

For production, consider migrating from JSON to a real database:

**PostgreSQL Migration:**
```python
# Install: pip install psycopg2-binary

import psycopg2
from app.models.database import db

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=edutrackx user=postgres password=secret")
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        name VARCHAR(255),
        ...
    )
''')

# Migrate data from JSON
for user in db.get_all('users'):
    cursor.execute(
        "INSERT INTO users (...) VALUES (...)",
        (user['email'], user['name'], ...)
    )

conn.commit()
```

## Performance Optimization

### Backend Optimizations

1. **Enable Caching:**
```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route('/api/dashboard/stats')
@cache.cached(timeout=300)
def get_stats():
    ...
```

2. **Database Indexing** (if using PostgreSQL/MongoDB)

3. **Use Redis for Sessions**

### Frontend Optimizations

1. **Code Splitting:**
Already configured with Vite

2. **Image Optimization:**
Use WebP format and lazy loading

3. **CDN for Static Assets:**
Deploy `dist` folder to CDN (Cloudflare, AWS CloudFront)

## Security Checklist

- [ ] Change JWT_SECRET_KEY to a strong random value
- [ ] Enable HTTPS/SSL
- [ ] Set secure CORS origins (not `*`)
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Regular security updates
- [ ] Input validation and sanitization
- [ ] SQL injection prevention (if using SQL)
- [ ] XSS protection headers
- [ ] CSRF tokens for forms

## Monitoring & Logging

### Application Monitoring

**Sentry Integration:**
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
)
```

### Log Management

**Use Python logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Scaling Strategies

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple Flask instances
- Use Gunicorn workers

### Database Scaling
- Read replicas
- Connection pooling
- Caching layer (Redis, Memcached)

### CDN for Frontend
- CloudFlare
- AWS CloudFront
- Vercel Edge Network

## Backup Strategy

1. **Database Backups:**
```bash
# Automated daily backups
0 2 * * * /usr/bin/python3 /path/to/backup_script.py
```

2. **Code Backups:**
- Use Git (GitHub, GitLab, Bitbucket)
- Automated deployments with GitHub Actions

## Health Checks

**Add health endpoint:**
```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
```

## Rollback Plan

1. Keep previous version tagged in Git
2. Have database migration rollback scripts
3. Use blue-green deployment strategy

## Support & Maintenance

- Set up error tracking (Sentry)
- Monitor server metrics (CPU, memory, disk)
- Regular dependency updates
- Security patches
- Performance monitoring

---

Choose the deployment option that best fits your needs and infrastructure!
