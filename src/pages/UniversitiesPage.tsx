import { useState } from 'react';
import { GraduationCap, MapPin, Award, Star, TrendingUp, Search } from 'lucide-react';
import { mockUniversityPrograms } from '../data/mockData';

export default function UniversitiesPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDiscipline, setSelectedDiscipline] = useState('All');

  const disciplines = ['All', 'Electrical Engineering', 'Mechanical Engineering', 'Computer Engineering', 'Civil Engineering', 'Software Engineering'];

  const filteredPrograms = mockUniversityPrograms.filter(program => {
    const matchesSearch = program.universityName.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         program.programName.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDiscipline = selectedDiscipline === 'All' || program.discipline === selectedDiscipline;
    return matchesSearch && matchesDiscipline;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">University Programs</h1>
        <p className="text-gray-600">
          Honest reviews and comprehensive information about engineering programs across Pakistan
        </p>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search universities or programs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
          <select
            value={selectedDiscipline}
            onChange={(e) => setSelectedDiscipline(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            {disciplines.map(discipline => (
              <option key={discipline} value={discipline}>{discipline}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Programs Grid */}
      <div className="grid gap-6">
        {filteredPrograms.map(program => (
          <div key={program.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
            {/* Header */}
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-900 mb-1">{program.universityName}</h3>
                  <p className="text-lg text-green-600 font-semibold">{program.degree} in {program.programName}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <Star className="w-5 h-5 text-yellow-500 fill-current" />
                  <span className="text-lg font-bold text-gray-900">{program.averageRating}</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <div className="flex items-center space-x-1">
                  <MapPin className="w-4 h-4" />
                  <span>{program.location}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <GraduationCap className="w-4 h-4" />
                  <span>{program.duration}</span>
                </div>
                {program.employabilityScore && (
                  <div className="flex items-center space-x-1">
                    <TrendingUp className="w-4 h-4" />
                    <span>Employability: {program.employabilityScore}%</span>
                  </div>
                )}
                <div className="flex items-center space-x-1">
                  <Award className="w-4 h-4" />
                  <span>{program.accreditation.join(', ')}</span>
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="p-6">
              <p className="text-gray-600 mb-4">{program.overview}</p>

              <div className="grid md:grid-cols-2 gap-6">
                {/* Pros */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    Strengths
                  </h4>
                  <ul className="space-y-1">
                    {program.pros.map((pro, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        <span>{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Cons */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                    <span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
                    Considerations
                  </h4>
                  <ul className="space-y-1">
                    {program.cons.map((con, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <span className="text-orange-600 mr-2">•</span>
                        <span>{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredPrograms.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <GraduationCap className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No programs found. Try adjusting your search.</p>
        </div>
      )}
    </div>
  );
}
