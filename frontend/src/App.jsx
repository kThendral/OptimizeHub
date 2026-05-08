import React, { useState, useEffect } from "react";
import LandingPage from "./components/LandingPage";
import AlgorithmSelector from "./components/AlgorithmSelector";
import LearnPage from "./pages/LearnPage";
import AuthModal from "./components/AuthModal";
import ProblemHistory from "./components/ProblemHistory";

function App() {
  const [currentPage, setCurrentPage] = useState(() => {
    const path = window.location.pathname;
    if (path === "/learn" || path === "/about") return "learn";
    if (path === "/app") return "app";
    return "landing";
  });

  // Auth state
  const [user, setUser] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);

  // Load user from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        console.error('Failed to parse user data:', e);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
  }, []);

  const handleAuth = (userData) => {
    setUser(userData);
    setShowAuthModal(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  // Handler to navigate to different pages
  const navigateToApp = () => {
    window.history.pushState({ page: 'app' }, '', '/app');
    setCurrentPage("app");
  };

  const navigateToLearn = () => {
    window.history.pushState({ page: 'learn' }, '', '/learn');
    setCurrentPage("learn");
  };

  const navigateToLanding = () => {
    window.history.pushState({ page: 'landing' }, '', '/');
    setCurrentPage("landing");
  };

  // Listen for browser back/forward and update view based on path
  React.useEffect(() => {
    const onPop = () => {
      const path = window.location.pathname;
      if (path === "/learn" || path === "/about") setCurrentPage("learn");
      else if (path === "/app") setCurrentPage("app");
      else setCurrentPage("landing");
    };

    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  if (currentPage === "landing") {
    return <LandingPage onStart={navigateToApp} onLearn={navigateToLearn} />;
  }

  if (currentPage === "learn") {
    return <LearnPage onBack={navigateToLanding} onStartOptimizing={navigateToApp} />;
  }

  return (
    <>
      <div className="min-h-screen bg-app py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          {/* Header with auth */}
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-4xl font-bold text-primary">OptimizeHub</h1>
            <div className="flex items-center gap-4">
              {user ? (
                <>
                  <span className="text-lg text-primary">
                    Hi {user.username || user.email}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 text-sm font-medium text-white bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setShowAuthModal(true)}
                  className="px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 rounded-lg transition-all transform hover:scale-105"
                >
                  Login / Sign Up
                </button>
              )}
            </div>
          </div>
          
          {/* Main Algorithm Selector with embedded forms and results */}
          <div className="card p-6 rounded-lg shadow-md">
            <AlgorithmSelector onHome={navigateToLanding} />
          </div>

          {/* Problem history for logged-in users */}
          <ProblemHistory user={user} />
        </div>
      </div>

      {/* Auth Modal */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuth={handleAuth}
      />
    </>
  );
}

export default App;
