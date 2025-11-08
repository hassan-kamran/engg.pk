import { Target, Users, Lightbulb, Heart, TrendingUp, Globe } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">About engg.pk</h1>
        <p className="text-xl text-gray-600">
          Building a community to empower Pakistani engineers and revive engineering excellence
        </p>
      </div>

      {/* Mission */}
      <div className="bg-gradient-to-br from-green-600 to-green-800 text-white rounded-lg p-8 mb-8">
        <div className="flex items-start space-x-4">
          <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0">
            <Target className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-bold mb-3">Our Mission</h2>
            <p className="text-green-100 leading-relaxed">
              To create a thriving community where Pakistani engineers can access curated knowledge,
              connect with experienced professionals, discover opportunities, and develop fulfilling
              careers in Pakistan. We aim to combat brain drain by showcasing the potential and
              opportunities within our country, while encouraging critical thinking and technical
              independence.
            </p>
          </div>
        </div>
      </div>

      {/* Vision */}
      <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Vision</h2>
        <p className="text-gray-700 leading-relaxed mb-4">
          We envision a Pakistan where engineers are empowered with knowledge, guided by experienced
          mentors, and equipped to build innovative solutions. A place where engineering excellence
          is celebrated, where students make informed decisions about their education and careers,
          and where the next generation of engineers contributes to national development while
          competing globally.
        </p>
        <p className="text-gray-700 leading-relaxed">
          We support engineers pursuing foreign education and international opportunities, but we
          want them to do so from a position of strength, critical thinking, and technical competence
          - not from colonial mindsets or lack of local opportunities.
        </p>
      </div>

      {/* Core Values */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Our Values</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Community First</h3>
            <p className="text-gray-600">
              We believe in the power of community. Engineers helping engineers, sharing knowledge,
              and supporting each other's growth.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <Lightbulb className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Expert Knowledge</h3>
            <p className="text-gray-600">
              All information is curated and verified by real experts - professionals who have
              walked the path and achieved success.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <Heart className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Honest & Transparent</h3>
            <p className="text-gray-600">
              We provide honest reviews, realistic expectations, and transparent information
              about programs, careers, and opportunities.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
              <TrendingUp className="w-5 h-5 text-orange-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Growth Mindset</h3>
            <p className="text-gray-600">
              We encourage continuous learning, skill development, and adaptation to industry
              changes and emerging technologies.
            </p>
          </div>
        </div>
      </div>

      {/* What We Offer */}
      <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">What We Offer</h2>
        <div className="space-y-4">
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">Community Forums</h3>
              <p className="text-gray-600">Discuss technical questions, career guidance, and industry insights</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">University Program Reviews</h3>
              <p className="text-gray-600">Honest reviews and comparisons of engineering programs across Pakistan</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">Career Path Guidance</h3>
              <p className="text-gray-600">Learn about different engineering careers from experienced professionals</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">Job Opportunities</h3>
              <p className="text-gray-600">Curated job listings across various engineering disciplines in Pakistan</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">Scholarship Database</h3>
              <p className="text-gray-600">Comprehensive information about scholarships for local and international studies</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">Industry Insights</h3>
              <p className="text-gray-600">Real-world applications and trends from industry experts</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">Subject Connections</h3>
              <p className="text-gray-600">Understanding how subjects relate and apply to real problems</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <span className="text-green-600 font-bold text-xl">•</span>
            <div>
              <h3 className="font-semibold text-gray-900">Startup Resources</h3>
              <p className="text-gray-600">Funding, incubation, and guidance for tech entrepreneurs</p>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-gradient-to-r from-green-600 to-green-700 text-white rounded-lg p-8 text-center">
        <Globe className="w-12 h-12 mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-3">Join Our Community</h2>
        <p className="text-green-100 mb-6">
          Be part of a movement to revive engineering excellence in Pakistan. Connect, learn, and grow with us.
        </p>
        <button className="bg-white text-green-700 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors">
          Get Started
        </button>
      </div>
    </div>
  );
}
