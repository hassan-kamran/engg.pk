import { Outlet, Link, useLocation } from 'react-router-dom';
import { Menu, X, Users, BookOpen, Briefcase, GraduationCap, Award, Lightbulb, Network, Rocket, MessageSquare } from 'lucide-react';
import { useState } from 'react';

export default function Layout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Home', href: '/', icon: Users },
    { name: 'Forum', href: '/forum', icon: MessageSquare },
    { name: 'Universities', href: '/universities', icon: GraduationCap },
    { name: 'Career Paths', href: '/careers', icon: Briefcase },
    { name: 'Jobs', href: '/jobs', icon: Briefcase },
    { name: 'Scholarships', href: '/scholarships', icon: Award },
    { name: 'Industry Insights', href: '/insights', icon: Lightbulb },
    { name: 'Subject Connections', href: '/subjects', icon: Network },
    { name: 'Startups', href: '/startups', icon: Rocket },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-green-700 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">E</span>
              </div>
              <div>
                <div className="text-xl font-bold text-gray-900">engg.pk</div>
                <div className="text-xs text-gray-500 hidden sm:block">Engineering Community of Pakistan</div>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex space-x-1">
              {navigation.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-green-50 text-green-700'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </nav>

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-md text-gray-700 hover:bg-gray-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="lg:hidden border-t border-gray-200 bg-white">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navigation.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium ${
                      isActive
                        ? 'bg-green-50 text-green-700'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main>
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">About engg.pk</h3>
              <p className="text-gray-600 text-sm">
                A community-driven platform for Pakistani engineers to connect, learn, and grow.
                Empowering engineers with knowledge, opportunities, and guidance.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Mission</h3>
              <p className="text-gray-600 text-sm">
                To revive engineering excellence in Pakistan, combat brain drain, and guide
                engineers towards fulfilling technical careers while promoting independence
                from colonial mindsets.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Links</h3>
              <ul className="space-y-2">
                <li><Link to="/about" className="text-gray-600 hover:text-green-600 text-sm">About Us</Link></li>
                <li><Link to="/forum" className="text-gray-600 hover:text-green-600 text-sm">Community Forum</Link></li>
                <li><Link to="/jobs" className="text-gray-600 hover:text-green-600 text-sm">Job Opportunities</Link></li>
                <li><Link to="/scholarships" className="text-gray-600 hover:text-green-600 text-sm">Scholarships</Link></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
            <p>&copy; 2024 engg.pk - Engineering Community of Pakistan. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
