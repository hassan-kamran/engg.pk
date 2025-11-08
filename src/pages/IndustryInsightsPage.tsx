import { Lightbulb, User, Eye, ThumbsUp, Calendar } from 'lucide-react';
import { mockIndustryInsights } from '../data/mockData';

export default function IndustryInsightsPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Industry Insights</h1>
        <p className="text-gray-600">
          Learn about real-world applications and industry trends from verified experts
        </p>
      </div>

      {/* Insights */}
      <div className="space-y-6">
        {mockIndustryInsights.map(insight => (
          <div key={insight.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
            {/* Header */}
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-start space-x-4 mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center text-white font-semibold">
                  {insight.author.name.split(' ').map(n => n[0]).join('')}
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{insight.title}</h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <div className="flex items-center space-x-1">
                      <User className="w-4 h-4" />
                      <span className="font-medium">{insight.author.name}</span>
                    </div>
                    {insight.author.verified && (
                      <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-medium rounded">
                        Verified {insight.author.role}
                      </span>
                    )}
                    <div className="flex items-center space-x-1">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(insight.createdAt).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 mb-2">
                <span className="px-3 py-1 bg-green-100 text-green-700 text-sm font-medium rounded-full">
                  {insight.industry}
                </span>
                <span className="px-3 py-1 bg-purple-100 text-purple-700 text-sm font-medium rounded-full">
                  {insight.discipline}
                </span>
              </div>

              <div className="flex flex-wrap gap-2">
                {insight.topics.map(topic => (
                  <span key={topic} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                    {topic}
                  </span>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="p-6">
              <p className="text-gray-700 leading-relaxed mb-4">{insight.content}</p>

              <div className="flex items-center space-x-6 text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <Eye className="w-4 h-4" />
                  <span>{insight.views} views</span>
                </div>
                <div className="flex items-center space-x-1">
                  <ThumbsUp className="w-4 h-4" />
                  <span>{insight.helpful} found this helpful</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {mockIndustryInsights.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <Lightbulb className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No insights available yet.</p>
        </div>
      )}
    </div>
  );
}
