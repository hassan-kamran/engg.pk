import { useState } from 'react';
import { Rocket, Building, DollarSign, BookOpen, Users, MapPin, ExternalLink } from 'lucide-react';
import { mockStartupResources } from '../data/mockData';
import { StartupResource } from '../types';

export default function StartupsPage() {
  const [selectedCategory, setSelectedCategory] = useState<StartupResource['category'] | 'All'>('All');

  const categories: (StartupResource['category'] | 'All')[] = [
    'All',
    'Funding',
    'Incubator',
    'Accelerator',
    'Mentorship',
    'Legal',
    'Technical',
    'Guide'
  ];

  const filteredResources = selectedCategory === 'All'
    ? mockStartupResources
    : mockStartupResources.filter(r => r.category === selectedCategory);

  const categoryIcons = {
    Funding: DollarSign,
    Incubator: Building,
    Accelerator: Rocket,
    Mentorship: Users,
    Legal: BookOpen,
    Technical: BookOpen,
    Guide: BookOpen
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Startup Resources</h1>
        <p className="text-gray-600">
          Access resources, funding opportunities, and guidance for building tech startups in Pakistan
        </p>
      </div>

      {/* Info Banner */}
      <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-bold mb-2">Build the Future</h2>
        <p className="text-purple-100 mb-4">
          Pakistan's startup ecosystem is growing rapidly. Whether you're building a tech product,
          seeking funding, or need guidance, we've curated resources to help you succeed.
        </p>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div>
            <div className="font-semibold mb-1">Growing Ecosystem</div>
            <div className="text-purple-100">National incubation centers across Pakistan</div>
          </div>
          <div>
            <div className="font-semibold mb-1">Funding Available</div>
            <div className="text-purple-100">Seed to Series A funding opportunities</div>
          </div>
          <div>
            <div className="font-semibold mb-1">Expert Mentorship</div>
            <div className="text-purple-100">Learn from successful entrepreneurs</div>
          </div>
        </div>
      </div>

      {/* Category Filter */}
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex flex-wrap gap-2">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedCategory === category
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Resources Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {filteredResources.map(resource => {
          const Icon = categoryIcons[resource.category];
          return (
            <div key={resource.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
              <div className="flex items-start space-x-4 mb-4">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Icon className="w-6 h-6 text-purple-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-lg font-bold text-gray-900">{resource.title}</h3>
                    <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded ml-2 flex-shrink-0">
                      {resource.category}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{resource.provider}</p>
                </div>
              </div>

              <p className="text-gray-700 mb-4">{resource.description}</p>

              {resource.location && (
                <div className="flex items-center space-x-2 text-sm text-gray-600 mb-3">
                  <MapPin className="w-4 h-4" />
                  <span>{resource.location}</span>
                </div>
              )}

              {resource.eligibility && (
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-900 mb-2">Eligibility:</h4>
                  <ul className="space-y-1">
                    {resource.eligibility.map((item, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <span className="text-purple-600 mr-2">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {resource.link && (
                <a
                  href={resource.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-2 text-purple-600 hover:text-purple-700 font-medium"
                >
                  <span>Learn More</span>
                  <ExternalLink className="w-4 h-4" />
                </a>
              )}
            </div>
          );
        })}
      </div>

      {filteredResources.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <Rocket className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No resources found in this category.</p>
        </div>
      )}
    </div>
  );
}
