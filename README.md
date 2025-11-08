# engg.pk - Engineering Community of Pakistan

A comprehensive community platform for Pakistani engineers to connect, learn, and grow together.

## Overview

engg.pk is designed to empower Pakistani engineers by providing:

- **Community Forum**: Discuss technical questions, career guidance, and industry insights
- **University Reviews**: Honest reviews and comparisons of engineering programs across Pakistan
- **Career Paths**: Learn about different engineering careers from experienced professionals
- **Job Board**: Discover engineering job opportunities across various industries
- **Scholarships**: Find scholarship opportunities for local and international studies
- **Industry Insights**: Real-world applications and trends from verified experts
- **Subject Connections**: Understand how subjects relate and apply to real problems
- **Startup Resources**: Funding, incubation, and guidance for tech entrepreneurs

## Mission

To create a thriving community where Pakistani engineers can access curated knowledge, connect with experienced professionals, discover opportunities, and develop fulfilling careers in Pakistan. We aim to combat brain drain by showcasing the potential within our country while encouraging critical thinking and technical independence.

## Features

### 🗣️ Community Forum
- Multiple categories: Technical Questions, Career Guidance, Industry Insights, Academia, Startups, etc.
- Expert-verified responses
- Upvoting and engagement tracking

### 🎓 University Programs
- Comprehensive reviews of engineering programs
- Pros and cons analysis
- Accreditation information
- Employability scores
- Student reviews and ratings

### 💼 Career Guidance
- Detailed career path information
- Skills required for different roles
- Salary ranges in Pakistan
- Industry insights and growth outlook
- Experience stories from professionals

### 🔍 Job Opportunities
- Curated engineering jobs across Pakistan
- Filter by discipline, type, and location
- Detailed job descriptions and requirements

### 🎖️ Scholarships
- Local and international scholarship opportunities
- Fully funded and partially funded programs
- Eligibility criteria and deadlines
- Application guidance

### 💡 Industry Insights
- Expert perspectives on industry trends
- Real-world applications of engineering concepts
- Case studies from power plants, tech companies, manufacturing, etc.

### 🔗 Subject Connections
- Understanding how subjects interconnect
- Real-world applications of academic concepts
- Career paths related to specific subjects

### 🚀 Startup Resources
- National incubation centers
- Funding opportunities
- Legal and technical resources
- Mentorship programs

## Technology Stack

**Why Django + HTMX?**

We chose Django + HTMX over React for several important reasons:
- **SEO-Friendly**: Server-side rendering means search engines can properly index our content (critical for discovering university reviews, scholarships, job postings)
- **Performance**: Faster initial page loads, especially on slower connections common in Pakistan
- **Simplicity**: One server handles everything - no complex frontend/backend split
- **Built-in Features**: Django Admin for content management, authentication, and security out of the box
- **Progressive Enhancement**: Works without JavaScript, degrades gracefully

### Backend
- **Django 5.x** - Python web framework with batteries included
- **PostgreSQL/SQLite** - Database (SQLite for development, PostgreSQL for production)
- **WhiteNoise** - Static file serving
- **Gunicorn** - Production WSGI server

### Frontend
- **Django Templates** - Server-side rendering for optimal SEO
- **HTMX** - Dynamic interactions without full page reloads (~14KB vs React's 140KB+)
- **Tailwind CSS** - Utility-first CSS framework (via CDN)
- **Alpine.js** - Lightweight JavaScript for complex UI interactions

### Key Benefits
- **Single Deployment**: One application to deploy and maintain
- **Better SEO**: All pages rendered server-side
- **Admin Panel**: Django Admin for content moderation
- **Faster Initial Loads**: Critical for users on slower connections

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip and virtualenv
- PostgreSQL (for production) or SQLite (for development)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hassan-kamran/engg.pk.git
cd engg.pk
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY and other settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

8. Open your browser and navigate to `http://localhost:8000`

### Access Admin Panel

- URL: `http://localhost:8000/admin/`
- Login with the superuser credentials you created

### Build for Production

1. Update settings for production (in `config/settings.py`):
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure PostgreSQL database
   - Set strong `SECRET_KEY`

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Run with Gunicorn:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Deployment Options

- **Railway** (recommended): Easy PostgreSQL integration
- **Render**: Free tier available
- **DigitalOcean App Platform**: Good for Pakistan region
- **Heroku**: Simple deployment with add-ons

## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

## Project Structure

```
engg.pk/
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # Core app (homepage, about, subjects)
├── forum/               # Community forum
├── universities/        # University program reviews
├── careers/             # Career paths
├── jobs/                # Job board
├── scholarships/        # Scholarship database
├── insights/            # Industry insights
├── startups/            # Startup resources
├── templates/           # Django templates
│   ├── base.html
│   ├── core/
│   ├── forum/
│   └── ...
├── static/              # Static files (CSS, JS, images)
├── manage.py
└── requirements.txt
```

## Future Enhancements

### Phase 1 (Immediate)
- Complete all page templates
- Add user authentication
- Implement HTMX-powered search and filtering
- Create data fixtures for sample content

### Phase 2 (Short-term)
- User profiles with expertise verification
- Post creation and editing via HTMX
- Like/upvote functionality
- Email notifications
- Image uploads for profiles and posts

### Phase 3 (Medium-term)
- Advanced search with Elasticsearch
- Real-time messaging (Django Channels)
- Mobile-responsive PWA
- Content moderation dashboard
- Analytics and insights

### Phase 4 (Long-term)
- API for mobile apps
- Recommendation engine
- Newsletter system
- Event management
- Mentorship matching

## License

MIT License - see LICENSE file for details

## Contact

For questions, suggestions, or collaboration opportunities, please reach out through our community forum or GitHub issues.

---

**Built with ❤️ for Pakistani Engineers**
