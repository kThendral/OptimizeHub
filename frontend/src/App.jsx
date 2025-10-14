import React, { useState } from "react";
import LandingPage from "./components/LandingPage";
import AlgorithmSelector from "./components/AlgorithmSelector";

function App() {
  const [showLanding, setShowLanding] = useState(() => {
    try {
      return window.location.pathname === "/";
    } catch (e) {
      return true;
    }
  });

  // Handler to navigate to app view and push history state so browser back works
  const navigateToApp = () => {
    try {
      window.history.pushState({ page: 'app' }, '', '/app');
    } catch (e) {
      /* ignore */
    }
    setShowLanding(false);
  };

  // Listen for browser back/forward and update view based on path
  React.useEffect(() => {
    const onPop = () => {
      setShowLanding(window.location.pathname === '/');
    };

    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  if (showLanding) {
    return <LandingPage onStart={navigateToApp} />;
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
