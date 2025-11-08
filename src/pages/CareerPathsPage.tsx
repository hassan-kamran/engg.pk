import { Briefcase, TrendingUp, BookOpen, DollarSign } from 'lucide-react';
import { mockCareerPaths } from '../data/mockData';

export default function CareerPathsPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Career Paths</h1>
        <p className="text-gray-600">
          Explore different engineering careers and learn from experienced professionals in Pakistan
        </p>
      </div>

      {/* Career Paths */}
      <div className="grid gap-6">
        {mockCareerPaths.map(career => (
          <div key={career.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <div className="p-6">
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-900 mb-1">{career.title}</h3>
                  <p className="text-green-600 font-medium">{career.discipline}</p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Briefcase className="w-6 h-6 text-green-600" />
                </div>
              </div>

              {/* Overview */}
              <p className="text-gray-600 mb-6">{career.overview}</p>

              {/* Details Grid */}
              <div className="grid md:grid-cols-2 gap-6 mb-6">
                {/* Skills */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                    <BookOpen className="w-4 h-4 mr-2 text-blue-600" />
                    Key Skills
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {career.skills.map(skill => (
                      <span key={skill} className="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Industries */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                    <Briefcase className="w-4 h-4 mr-2 text-purple-600" />
                    Industries
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {career.industries.map(industry => (
                      <span key={industry} className="px-3 py-1 bg-purple-50 text-purple-700 text-sm rounded-full">
                        {industry}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Salary and Growth */}
              <div className="grid md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="flex items-start space-x-3">
                  <DollarSign className="w-5 h-5 text-green-600 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-600">Salary Range in Pakistan</div>
                    <div className="font-semibold text-gray-900">{career.salaryRange}</div>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <TrendingUp className="w-5 h-5 text-green-600 mt-0.5" />
                  <div>
                    <div className="text-sm text-gray-600">Growth Outlook</div>
                    <div className="font-semibold text-gray-900">{career.growthOutlook}</div>
                  </div>
                </div>
              </div>

              {/* Education Required */}
              <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                <div className="text-sm text-blue-900 font-medium mb-1">Education Required</div>
                <div className="text-blue-700">{career.educationRequired}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
