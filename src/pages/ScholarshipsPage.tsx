import { useState } from 'react';
import { Award, Globe, GraduationCap, Calendar, DollarSign, Search, ExternalLink } from 'lucide-react';
import { mockScholarships } from '../data/mockData';

export default function ScholarshipsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('All');

  const levels = ['All', 'Undergraduate', 'Graduate', 'Doctoral', 'Postdoctoral'];

  const filteredScholarships = mockScholarships.filter(scholarship => {
    const matchesSearch = scholarship.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         scholarship.provider.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         scholarship.country.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesLevel = selectedLevel === 'All' || scholarship.level === selectedLevel;
    return matchesSearch && matchesLevel;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Scholarships</h1>
        <p className="text-gray-600">
          Discover scholarship opportunities for engineering students
        </p>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search scholarships..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
          <select
            value={selectedLevel}
            onChange={(e) => setSelectedLevel(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            {levels.map(level => (
              <option key={level} value={level}>{level}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Scholarships Grid */}
      <div className="grid gap-6">
        {filteredScholarships.map(scholarship => (
          <div key={scholarship.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-xl font-bold text-gray-900 mb-1">{scholarship.name}</h3>
                <p className="text-gray-600 font-medium">{scholarship.provider}</p>
              </div>
              <span className={`px-3 py-1 text-sm font-medium rounded-full ${
                scholarship.funded === 'Fully Funded'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-yellow-100 text-yellow-700'
              }`}>
                {scholarship.funded}
              </span>
            </div>

            {/* Info Grid */}
            <div className="grid md:grid-cols-2 gap-4 mb-4">
              <div className="flex items-center space-x-2 text-gray-600">
                <Globe className="w-4 h-4" />
                <span>{scholarship.country}</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <GraduationCap className="w-4 h-4" />
                <span>{scholarship.level}</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <DollarSign className="w-4 h-4" />
                <span>{scholarship.amount}</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <Calendar className="w-4 h-4" />
                <span>Deadline: {new Date(scholarship.deadline).toLocaleDateString()}</span>
              </div>
            </div>

            {/* Disciplines */}
            <div className="mb-4">
              <div className="flex flex-wrap gap-2">
                {scholarship.disciplines.map(discipline => (
                  <span key={discipline} className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
                    {discipline}
                  </span>
                ))}
              </div>
            </div>

            {/* Description */}
            <p className="text-gray-600 mb-4">{scholarship.description}</p>

            {/* Eligibility */}
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Eligibility:</h4>
              <ul className="space-y-1">
                {scholarship.eligibility.map((item, index) => (
                  <li key={index} className="text-sm text-gray-600 flex items-start">
                    <span className="text-green-600 mr-2">✓</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Apply Button */}
            <a
              href={scholarship.applicationUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <span>Learn More</span>
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        ))}
      </div>

      {filteredScholarships.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <Award className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No scholarships found. Try adjusting your search.</p>
        </div>
      )}
    </div>
  );
}
