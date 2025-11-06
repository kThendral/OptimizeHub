import React, { useState } from "react";
import LandingPage from "./components/LandingPage";
import AlgorithmSelector from "./components/AlgorithmSelector";
import LearnPage from "./pages/LearnPage";

function App() {
  const [currentPage, setCurrentPage] = useState(() => {
    const path = window.location.pathname;
    if (path === "/learn" || path === "/about") return "learn";
    if (path === "/app") return "app";
    return "landing";
  });

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
    <div className="min-h-screen bg-app py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold text-primary mb-8 text-center">OptimizeHub</h1>
        
        {/* Main Algorithm Selector with embedded forms and results */}
        <div className="card p-6 rounded-lg shadow-md">
          <AlgorithmSelector />
        </div>
      </div>
    </div>
  );
}

export default App;
