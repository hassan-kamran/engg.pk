import { Network, BookOpen, Briefcase, Code } from 'lucide-react';
import { mockSubjectConnections } from '../data/mockData';

export default function SubjectConnectionsPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Subject Connections</h1>
        <p className="text-gray-600">
          Understand how different engineering subjects connect and apply to real-world problems
        </p>
      </div>

      {/* Subject Connections */}
      <div className="space-y-6">
        {mockSubjectConnections.map(subject => (
          <div key={subject.id} className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
            {/* Header */}
            <div className="flex items-start space-x-4 mb-4">
              <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
                <Network className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{subject.subject}</h3>
                <p className="text-gray-600">{subject.description}</p>
              </div>
            </div>

            {/* Related Subjects */}
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <BookOpen className="w-4 h-4 mr-2 text-blue-600" />
                Related Subjects
              </h4>
              <div className="flex flex-wrap gap-2">
                {subject.relatedSubjects.map(related => (
                  <span key={related} className="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full">
                    {related}
                  </span>
                ))}
              </div>
            </div>

            {/* Applications */}
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <Code className="w-4 h-4 mr-2 text-purple-600" />
                Real-World Applications
              </h4>
              <div className="grid md:grid-cols-2 gap-2">
                {subject.applications.map((application, index) => (
                  <div key={index} className="flex items-start space-x-2">
                    <span className="text-purple-600 mt-1">•</span>
                    <span className="text-gray-700">{application}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Career Paths */}
            <div>
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <Briefcase className="w-4 h-4 mr-2 text-green-600" />
                Related Career Paths
              </h4>
              <div className="flex flex-wrap gap-2">
                {subject.careerPaths.map(career => (
                  <span key={career} className="px-3 py-1 bg-green-50 text-green-700 text-sm rounded-full">
                    {career}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
