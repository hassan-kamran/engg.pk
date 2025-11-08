from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from core.models import UserProfile, SubjectConnection
from forum.models import ForumPost, Reply
from universities.models import UniversityProgram, ProgramReview
from careers.models import CareerPath, ExperienceStory
from jobs.models import Job
from scholarships.models import Scholarship
from insights.models import IndustryInsight
from startups.models import StartupResource


class Command(BaseCommand):
    help = 'Load sample data for demonstration'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@engg.pk',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if _:
            admin_user.set_password('admin123')
            admin_user.save()

        dr_ahmed, _ = User.objects.get_or_create(
            username='dr_ahmed',
            defaults={
                'first_name': 'Ahmed',
                'last_name': 'Khan',
                'email': 'ahmed.khan@nust.edu.pk'
            }
        )
        UserProfile.objects.get_or_create(
            user=dr_ahmed,
            defaults={
                'role': 'expert',
                'expertise': ['Power Systems', 'Control Systems', 'Renewable Energy'],
                'affiliation': 'NUST Islamabad',
                'verified': True,
                'bio': 'Professor of Electrical Engineering with 15 years of experience in power systems and renewable energy.'
            }
        )

        fatima, _ = User.objects.get_or_create(
            username='fatima_malik',
            defaults={
                'first_name': 'Fatima',
                'last_name': 'Malik',
                'email': 'fatima.malik@techsolutions.pk'
            }
        )
        UserProfile.objects.get_or_create(
            user=fatima,
            defaults={
                'role': 'professional',
                'expertise': ['Software Engineering', 'Cloud Computing'],
                'affiliation': 'Tech Solutions Pvt Ltd',
                'verified': True,
                'bio': 'Senior Software Engineer working on cloud infrastructure and distributed systems.'
            }
        )

        # Create forum posts
        ForumPost.objects.get_or_create(
            title='How to maintain control systems in gas-fired power plants?',
            defaults={
                'content': 'I recently joined a power plant as a maintenance engineer. I would like to understand the best practices for maintaining DCS and SCADA systems in gas-fired power plants. What are the common challenges and how to address them?',
                'author': fatima,
                'category': 'technical',
                'tags': ['Power Plant', 'Control Systems', 'Maintenance'],
                'views': 234
            }
        )

        ForumPost.objects.get_or_create(
            title='Career paths in Pakistan for Mechanical Engineers',
            defaults={
                'content': 'I am about to graduate with a BS in Mechanical Engineering. What are the best career opportunities available in Pakistan? Should I focus on industry or consider further studies?',
                'author': dr_ahmed,
                'category': 'career',
                'tags': ['Mechanical Engineering', 'Career', 'Pakistan'],
                'views': 567
            }
        )

        # Create university programs
        UniversityProgram.objects.get_or_create(
            university_name='NUST',
            program_name='Electrical Engineering',
            degree='BS',
            defaults={
                'discipline': 'Electrical Engineering',
                'location': 'Islamabad',
                'accreditation': ['PEC', 'HEC'],
                'duration': '4 years',
                'overview': 'Comprehensive program covering power systems, electronics, control systems, and telecommunications.',
                'pros': [
                    'Strong faculty with industry experience',
                    'Well-equipped labs and modern facilities',
                    'Good placement record in top companies',
                    'Research opportunities available',
                    'Strong alumni network'
                ],
                'cons': [
                    'Highly competitive admission',
                    'Intense workload',
                    'Limited flexibility in course selection',
                    'High fee structure compared to public universities'
                ],
                'employability_score': 85,
                'research_opportunities': True
            }
        )

        UniversityProgram.objects.get_or_create(
            university_name='UET Lahore',
            program_name='Mechanical Engineering',
            degree='BS',
            defaults={
                'discipline': 'Mechanical Engineering',
                'location': 'Lahore',
                'accreditation': ['PEC', 'HEC'],
                'duration': '4 years',
                'overview': 'Traditional mechanical engineering program with focus on thermal systems, manufacturing, and design.',
                'pros': [
                    'Oldest engineering university in Pakistan',
                    'Strong industry connections',
                    'Affordable fee structure',
                    'Excellent lab facilities'
                ],
                'cons': [
                    'Traditional teaching methods',
                    'Large class sizes',
                    'Limited exposure to modern software tools'
                ],
                'employability_score': 78,
                'research_opportunities': True
            }
        )

        # Create career paths
        CareerPath.objects.get_or_create(
            title='Power Plant Engineer',
            defaults={
                'discipline': 'Electrical Engineering',
                'overview': 'Power plant engineers operate, maintain, and optimize electrical power generation facilities including thermal, hydro, and renewable energy plants.',
                'skills': ['Control Systems', 'Power Systems', 'SCADA', 'DCS', 'Preventive Maintenance'],
                'industries': ['Energy', 'Utilities', 'Oil & Gas'],
                'salary_range': 'PKR 50,000 - 250,000/month',
                'growth_outlook': 'Steady growth with increasing demand for renewable energy expertise',
                'education_required': 'BS in Electrical Engineering, certifications in control systems preferred'
            }
        )

        CareerPath.objects.get_or_create(
            title='Software Engineer',
            defaults={
                'discipline': 'Computer Science',
                'overview': 'Develop software applications, systems, and solutions for various platforms and industries.',
                'skills': ['Programming', 'Data Structures', 'Algorithms', 'Web Development', 'Cloud Computing'],
                'industries': ['Technology', 'Finance', 'E-commerce', 'Healthcare'],
                'salary_range': 'PKR 40,000 - 500,000/month',
                'growth_outlook': 'Excellent growth with high demand locally and internationally',
                'education_required': 'BS in Computer Science/Software Engineering or equivalent'
            }
        )

        # Create jobs
        Job.objects.get_or_create(
            title='Maintenance Engineer - Power Plant',
            defaults={
                'company': 'Sahiwal Coal Power Plant',
                'location': 'Sahiwal, Punjab',
                'job_type': 'full-time',
                'discipline': 'Electrical Engineering',
                'experience_level': 'mid',
                'description': 'Responsible for maintaining and troubleshooting control systems, switchgear, and electrical equipment in a 1320MW coal-fired power plant.',
                'requirements': [
                    'BS in Electrical Engineering',
                    '3-5 years experience in power plant maintenance',
                    'Knowledge of DCS, SCADA, and PLC systems'
                ],
                'salary': 'PKR 120,000 - 180,000/month',
                'application_url': 'https://example.com/apply'
            }
        )

        Job.objects.get_or_create(
            title='Software Engineer - Full Stack',
            defaults={
                'company': 'Systems Limited',
                'location': 'Lahore, Punjab',
                'job_type': 'full-time',
                'discipline': 'Software Engineering',
                'experience_level': 'entry',
                'description': 'Join our development team to build modern web applications using React, Node.js, and cloud technologies.',
                'requirements': [
                    'BS in Computer Science or related field',
                    'Proficiency in JavaScript/TypeScript',
                    'Experience with React and Node.js'
                ],
                'salary': 'PKR 60,000 - 90,000/month',
                'application_url': 'https://example.com/apply'
            }
        )

        # Create scholarships
        Scholarship.objects.get_or_create(
            name='HEC Indigenous PhD Fellowship',
            defaults={
                'provider': 'Higher Education Commission Pakistan',
                'country': 'Pakistan',
                'level': 'doctoral',
                'disciplines': ['All Engineering Disciplines'],
                'amount': 'PKR 25,000/month stipend + tuition',
                'deadline': timezone.now().date() + timedelta(days=90),
                'description': 'Fellowship program for Pakistani students to pursue PhD in Pakistani universities.',
                'eligibility': [
                    'Pakistani national',
                    'MS/MPhil degree with minimum 3.0 CGPA',
                    'Admission in HEC-recognized university',
                    'Age limit: 35 years'
                ],
                'application_url': 'https://hec.gov.pk',
                'funded': 'fully'
            }
        )

        Scholarship.objects.get_or_create(
            name='DAAD Master\'s Scholarships',
            defaults={
                'provider': 'DAAD Germany',
                'country': 'Germany',
                'level': 'graduate',
                'disciplines': ['Engineering', 'Technology', 'Sciences'],
                'amount': '€934/month + insurance + travel',
                'deadline': timezone.now().date() + timedelta(days=60),
                'description': 'Scholarships for international students to pursue Master\'s degrees in Germany.',
                'eligibility': [
                    'Bachelor\'s degree with good academic record',
                    'At least 2 years work experience preferred',
                    'IELTS/TOEFL or German language proficiency'
                ],
                'application_url': 'https://www.daad.de',
                'funded': 'fully'
            }
        )

        # Create industry insights
        IndustryInsight.objects.get_or_create(
            title='The Future of Power Generation in Pakistan',
            defaults={
                'industry': 'Energy',
                'content': 'Pakistan is transitioning towards renewable energy with targets of 30% renewable energy by 2030. This shift creates opportunities for engineers skilled in solar, wind, and hybrid systems. The control systems in modern power plants are becoming increasingly sophisticated, requiring engineers to understand both traditional power systems and modern automation technologies. Engineers who can bridge this gap will find excellent career opportunities in the coming years.',
                'author': dr_ahmed,
                'discipline': 'Electrical Engineering',
                'topics': ['Renewable Energy', 'Power Systems', 'Control Systems'],
                'views': 1245,
                'helpful_count': 89
            }
        )

        IndustryInsight.objects.get_or_create(
            title='Pakistan\'s Growing Tech Industry: Opportunities and Challenges',
            defaults={
                'industry': 'Technology',
                'content': 'Pakistan\'s IT industry has grown to $3.5 billion in exports, with a growth rate of 25% annually. However, there is a significant skill gap in areas like cloud computing, AI/ML, and cybersecurity. Engineers who upskill in these areas have excellent opportunities both locally and internationally. The key is to focus on practical skills and building a strong portfolio.',
                'author': fatima,
                'discipline': 'Software Engineering',
                'topics': ['Software Development', 'Cloud Computing', 'Career Growth'],
                'views': 2134,
                'helpful_count': 156
            }
        )

        # Create subject connections
        SubjectConnection.objects.get_or_create(
            subject='Control Systems',
            defaults={
                'description': 'Control systems theory forms the foundation for automated systems across all industries. Understanding feedback, stability, and control design is crucial for modern engineering applications.',
                'related_subjects': ['Signals and Systems', 'Mathematics', 'Power Electronics', 'Digital Signal Processing'],
                'applications': [
                    'Power plant automation',
                    'Industrial process control',
                    'Robotics',
                    'Automotive systems',
                    'HVAC systems'
                ],
                'career_paths': ['Power Plant Engineer', 'Automation Engineer', 'Robotics Engineer']
            }
        )

        SubjectConnection.objects.get_or_create(
            subject='Data Structures and Algorithms',
            defaults={
                'description': 'Core computer science subject essential for efficient problem-solving and software development. Critical for technical interviews and system design.',
                'related_subjects': ['Programming Fundamentals', 'Discrete Mathematics', 'Database Systems', 'Operating Systems'],
                'applications': [
                    'Software development',
                    'System design',
                    'Database optimization',
                    'AI and machine learning',
                    'Network routing'
                ],
                'career_paths': ['Software Engineer', 'Data Engineer', 'Backend Developer', 'System Architect']
            }
        )

        # Create startup resources
        StartupResource.objects.get_or_create(
            title='National Incubation Centers (NICs)',
            defaults={
                'category': 'incubator',
                'description': 'Nationwide incubation centers providing workspace, mentorship, and funding opportunities for tech startups.',
                'provider': 'Ignite - National Technology Fund',
                'link': 'https://ignite.org.pk',
                'eligibility': ['Tech-based startup idea', 'Team of 2-5 members', 'Pakistani nationals'],
                'location': 'Islamabad, Lahore, Karachi, Peshawar, Quetta'
            }
        )

        StartupResource.objects.get_or_create(
            title='Startup Pakistan Portal',
            defaults={
                'category': 'guide',
                'description': 'Government portal for startup registration, licensing, and regulatory compliance.',
                'provider': 'SECP Pakistan',
                'link': 'https://startup.secp.gov.pk',
                'eligibility': ['Any Pakistani entrepreneur'],
                'location': 'Online'
            }
        )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
