import React, { useState } from 'react';

export default function HamburgerMenu({ sections, activeSection, onSectionChange, className = '' }) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleSectionClick = (sectionId) => {
    onSectionChange(sectionId);
    setIsOpen(false); // Close menu on mobile after selection
  };

  return (
    <div className={`relative ${className}`}>
      {/* Hamburger Button - Mobile Only */}
      <button
        onClick={toggleMenu}
        className="md:hidden p-2 rounded-lg hover:bg-purple-50 transition-all focus:outline-none focus:ring-2 focus:ring-purple-300"
        aria-label="Toggle menu"
      >
        <svg 
          className={`w-6 h-6 text-gray-600 transition-transform duration-300 ${isOpen ? 'rotate-90' : ''}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          {isOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      {/* Desktop Navigation - Always Visible */}
      <nav className="hidden md:flex space-x-6">
        {sections.map((section) => (
          <button
            key={section.id}
            onClick={() => handleSectionClick(section.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 ${
              activeSection === section.id
                ? 'bg-gradient-to-r from-purple-100 to-blue-100 text-purple-800 shadow-sm'
                : 'text-gray-600 hover:text-purple-800 hover:bg-purple-50'
            }`}
          >
            <span className="text-lg">{section.icon}</span>
            <span>{section.label}</span>
          </button>
        ))}
      </nav>

      {/* Mobile Dropdown Menu */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="md:hidden fixed inset-0 bg-black bg-opacity-25 z-40"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Menu Panel */}
          <div className="md:hidden absolute top-full right-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 overflow-hidden">
            <nav className="py-2">
              {sections.map((section, index) => (
                <button
                  key={section.id}
                  onClick={() => handleSectionClick(section.id)}
                  className={`w-full text-left px-6 py-4 font-medium transition-all duration-200 flex items-center gap-3 ${
                    activeSection === section.id
                      ? 'bg-gradient-to-r from-purple-50 to-blue-50 text-purple-800 border-r-4 border-purple-500'
                      : 'text-gray-700 hover:bg-purple-50 hover:text-purple-800'
                  } ${index !== sections.length - 1 ? 'border-b border-gray-100' : ''}`}
                >
                  <span className="text-xl">{section.icon}</span>
                  <span>{section.label}</span>
                  {activeSection === section.id && (
                    <svg className="w-4 h-4 ml-auto text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              ))}
            </nav>
          </div>
        </>
      )}
    </div>
  );
}

// Alternative sidebar version for larger screens
export function SidebarMenu({ sections, activeSection, onSectionChange, className = '' }) {
  return (
    <aside className={`w-64 bg-white/80 backdrop-blur-sm border-r border-purple-100 ${className}`}>
      <nav className="p-4 space-y-2">
        {sections.map((section) => (
          <button
            key={section.id}
            onClick={() => onSectionChange(section.id)}
            className={`w-full text-left px-4 py-3 rounded-xl font-medium transition-all duration-200 flex items-center gap-3 ${
              activeSection === section.id
                ? 'bg-gradient-to-r from-purple-100 to-blue-100 text-purple-800 shadow-sm'
                : 'text-gray-600 hover:text-purple-800 hover:bg-purple-50'
            }`}
          >
            <span className="text-xl">{section.icon}</span>
            <span>{section.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
}