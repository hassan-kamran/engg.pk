#!/usr/bin/env python
"""
Setup script to create test data for the infinite scroll feed feature
Run with: python manage.py shell < setup_feed_data.py
"""

from django.contrib.auth.models import User
from feed.models import ThoughtLeader, ProfessionalBody, FeedPost, UserSubscription, OrganizationSubscription
from core.models import UserProfile

print("\n" + "="*60)
print("🚀 CREATING TEST DATA FOR INFINITE SCROLL FEED")
print("="*60 + "\n")

# Create thought leader users and profiles
print("📝 Creating thought leaders...")

leader_users = []
for i, (username, first, last, title, org, bio, areas, followers) in enumerate([
    ('john_doe', 'John', 'Doe', 'Senior Software Engineer', 'Google',
     'Expert in distributed systems and cloud architecture. 10+ years building scalable systems.',
     ['Python', 'Django', 'Kubernetes', 'AWS'], 5420),
    ('jane_smith', 'Jane', 'Smith', 'Lead Electrical Engineer', 'Tesla',
     'Passionate about renewable energy and sustainable power systems',
     ['Power Systems', 'Renewable Energy', 'Circuit Design'], 3210),
    ('ali_khan', 'Ali', 'Khan', 'Chief Technology Officer', 'Systems Limited',
     'Building the next generation of Pakistani tech companies',
     ['Leadership', 'Strategy', 'Innovation'], 8750),
]):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first,
            'last_name': last,
            'email': f'{username}@example.com',
            'password': 'pbkdf2_sha256$600000$test$test'
        }
    )

    if created:
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'professional', 'affiliation': org}
        )

        leader, _ = ThoughtLeader.objects.get_or_create(
            user=user,
            defaults={
                'title': title,
                'organization': org,
                'bio': bio,
                'expertise_areas': areas,
                'verified': True,
                'follower_count': followers
            }
        )
        print(f"   ✅ {first} {last} - {title}")
        leader_users.append(user)
    else:
        leader_users.append(user)
        print(f"   ⏭️  {username} already exists")

# Create professional bodies/organizations
print("\n📝 Creating professional organizations...")

for name, slug, category, desc, followers in [
    ('Pakistan Engineering Council', 'pec', 'association',
     'The regulatory body for engineering profession in Pakistan. Ensuring standards and professional development.', 12500),
    ('NUST', 'nust', 'university',
     'National University of Sciences and Technology - Premier engineering university in Pakistan', 8900),
    ('Systems Limited', 'systems-limited', 'company',
     'Leading Pakistani software development company with global clients', 4200),
    ('LUMS', 'lums', 'university',
     'Lahore University of Management Sciences', 7100),
]:
    org, created = ProfessionalBody.objects.get_or_create(
        slug=slug,
        defaults={
            'name': name,
            'category': category,
            'description': desc,
            'verified': True,
            'follower_count': followers
        }
    )
    if created:
        print(f"   ✅ {name}")
    else:
        print(f"   ⏭️  {name} already exists")

# Get the test user
test_user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)
if created:
    test_user.set_password('testpass123')
    test_user.save()
    UserProfile.objects.get_or_create(
        user=test_user,
        defaults={'role': 'student', 'affiliation': 'NUST'}
    )
    print(f"\n✅ Created test user: testuser (password: testpass123)")
else:
    print(f"\n⏭️  Test user already exists: testuser")

# Subscribe test user to leaders
print("\n📝 Setting up subscriptions...")
for leader_user in leader_users[:2]:  # Subscribe to first 2 leaders
    try:
        leader = ThoughtLeader.objects.get(user=leader_user)
        sub, created = UserSubscription.objects.get_or_create(
            subscriber=test_user,
            thought_leader=leader
        )
        if created:
            leader.follower_count += 1
            leader.save()
            print(f"   ✅ Subscribed to {leader_user.get_full_name()}")
        else:
            print(f"   ⏭️  Already subscribed to {leader_user.get_full_name()}")
    except ThoughtLeader.DoesNotExist:
        print(f"   ❌ Leader not found for {leader_user.username}")

# Create feed posts
print("\n📝 Creating feed posts...")
existing_posts = FeedPost.objects.count()

if existing_posts < 25:
    posts_to_create = 25 - existing_posts
    print(f"   Creating {posts_to_create} posts...")

    for i in range(posts_to_create):
        idx = existing_posts + i
        if idx % 3 == 0:
            FeedPost.objects.create(
                author_user=leader_users[0],
                post_type='article',
                title=f'Software Architecture Patterns #{idx+1}',
                content=f'''In this article, we explore fundamental software architecture patterns that every engineer should master.

Key topics:
- Microservices architecture
- Event-driven design
- CQRS and Event Sourcing
- Scalability considerations
- Real-world case studies

This knowledge is essential for senior engineers and architects.''',
                topics=['software', 'architecture', 'engineering'],
                views=320 + idx*10
            )
        elif idx % 3 == 1:
            FeedPost.objects.create(
                author_user=leader_users[1],
                post_type='insight',
                title=f'Renewable Energy in Pakistan #{idx+1}',
                content=f'''Pakistan has enormous potential for renewable energy development.

Key insights:
- Current renewable energy capacity
- Government initiatives
- Technical challenges
- Investment opportunities
- Environmental impact

Join the discussion on accelerating Pakistan's renewable energy transition.''',
                topics=['renewable', 'energy', 'pakistan'],
                views=250 + idx*8
            )
        else:
            org = ProfessionalBody.objects.filter(slug='systems-limited').first()
            FeedPost.objects.create(
                author_organization=org,
                post_type='announcement',
                title=f'Engineering Positions Open #{idx+1}',
                content=f'''Multiple openings for talented engineers at Systems Limited!

Positions:
- Senior Software Engineers
- DevOps Engineers
- Data Engineers
- QA Engineers

Apply today for competitive salaries and benefits!''',
                topics=['jobs', 'career', 'pakistan'],
                views=180 + idx*12
            )
    print(f"   ✅ Created {posts_to_create} new posts")
else:
    print(f"   ⏭️  Already have {existing_posts} posts")

# Summary
print("\n" + "="*60)
print("✅ SETUP COMPLETE!")
print("="*60)
print(f"\n📊 Database Summary:")
print(f"   • Users: {User.objects.count()}")
print(f"   • Thought Leaders: {ThoughtLeader.objects.count()}")
print(f"   • Organizations: {ProfessionalBody.objects.count()}")
print(f"   • Feed Posts: {FeedPost.objects.count()}")
print(f"   • Subscriptions: {UserSubscription.objects.count()}")

print(f"\n🎯 Next Steps:")
print(f"   1. Login as: testuser / testpass123")
print(f"   2. Visit: http://localhost:8000/feed/")
print(f"   3. Scroll down to see infinite scroll in action!")
print(f"   4. Browse: /feed/thought-leaders/")
print(f"   5. Browse: /feed/organizations/")
print()
