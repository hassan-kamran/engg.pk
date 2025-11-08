import { Link } from 'react-router-dom';
import { MessageSquare, GraduationCap, Briefcase, Award, Lightbulb, Rocket, TrendingUp, Users } from 'lucide-react';

export default function HomePage() {
  const features = [
    {
      icon: MessageSquare,
      title: 'Community Forum',
      description: 'Discuss technical questions, career guidance, and industry insights with fellow engineers.',
      link: '/forum',
      color: 'bg-blue-500'
    },
    {
      icon: GraduationCap,
      title: 'University Reviews',
      description: 'Read honest reviews and comparisons of engineering programs across Pakistan.',
      link: '/universities',
      color: 'bg-purple-500'
    },
    {
      icon: Briefcase,
      title: 'Career Paths',
      description: 'Explore different engineering careers and learn from experienced professionals.',
      link: '/careers',
      color: 'bg-green-500'
    },
    {
      icon: Briefcase,
      title: 'Job Board',
      description: 'Find engineering job opportunities across Pakistan in various industries.',
      link: '/jobs',
      color: 'bg-orange-500'
    },
    {
      icon: Award,
      title: 'Scholarships',
      description: 'Discover scholarship opportunities for undergraduate and graduate studies.',
      link: '/scholarships',
      color: 'bg-yellow-500'
    },
    {
      icon: Lightbulb,
      title: 'Industry Insights',
      description: 'Learn about real-world applications and industry trends from experts.',
      link: '/insights',
      color: 'bg-red-500'
    },
    {
      icon: TrendingUp,
      title: 'Subject Connections',
      description: 'Understand how different subjects connect and apply to real-world problems.',
      link: '/subjects',
      color: 'bg-indigo-500'
    },
    {
      icon: Rocket,
      title: 'Startup Resources',
      description: 'Access resources, funding opportunities, and guidance for tech startups.',
      link: '/startups',
      color: 'bg-pink-500'
    }
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-green-600 to-green-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Engineering Community of Pakistan
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-green-100 max-w-3xl mx-auto">
              Empowering Pakistani engineers with knowledge, opportunities, and community.
              Together, we can revive engineering excellence and build a stronger Pakistan.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                to="/forum"
                className="bg-white text-green-700 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors inline-flex items-center space-x-2"
              >
                <MessageSquare className="w-5 h-5" />
                <span>Join the Forum</span>
              </Link>
              <Link
                to="/about"
                className="bg-green-700 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-800 transition-colors border-2 border-white"
              >
                Learn More
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-white py-12 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">1000+</div>
              <div className="text-gray-600">Community Members</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">50+</div>
              <div className="text-gray-600">University Programs</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">200+</div>
              <div className="text-gray-600">Job Listings</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">100+</div>
              <div className="text-gray-600">Scholarships</div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-lg text-gray-600">
              We believe in empowering Pakistani engineers to excel in their fields, contribute to national
              development, and compete globally while maintaining their technical independence and critical thinking.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <Users className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Connect Engineers</h3>
              <p className="text-gray-600">
                Build a strong community where students, professionals, and experts can share knowledge and experiences.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Lightbulb className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Share Knowledge</h3>
              <p className="text-gray-600">
                Provide curated, expert-verified information about education, careers, and technical topics.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Combat Brain Drain</h3>
              <p className="text-gray-600">
                Showcase opportunities in Pakistan and guide engineers towards fulfilling local careers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Explore Our Platform</h2>
            <p className="text-lg text-gray-600">
              Everything you need to navigate your engineering journey in Pakistan
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <Link
                  key={feature.title}
                  to={feature.link}
                  className="group bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-all hover:border-green-300"
                >
                  <div className={`w-12 h-12 ${feature.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-sm text-gray-600">{feature.description}</p>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-green-600 to-green-700 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Join the Community?</h2>
          <p className="text-xl text-green-100 mb-8">
            Connect with fellow engineers, access expert knowledge, and take control of your engineering career.
          </p>
          <Link
            to="/forum"
            className="bg-white text-green-700 px-8 py-4 rounded-lg font-semibold hover:bg-green-50 transition-colors inline-flex items-center space-x-2 text-lg"
          >
            <MessageSquare className="w-6 h-6" />
            <span>Start Exploring</span>
          </Link>
        </div>
      </section>
    </div>
  );
}
