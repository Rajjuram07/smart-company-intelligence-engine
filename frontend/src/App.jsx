import React, { useState, useEffect } from 'react';
import CompanyCard from './components/CompanyCard';
import Login from './components/Login';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [companyData, setCompanyData] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const auth = localStorage.getItem('auth');
    if (auth === 'true') {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('auth');
    setIsAuthenticated(false);
    window.location.reload();
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;

    setLoading(true);
    setError('');
    setCompanyData(null);

    try {
      // Use the environment variable for the backend API URL
      // const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const apiUrl = 'https://smart-company-intelligence-engine-3.onrender.com';
      const modeApiKey = import.meta.env.VITE_APP_API_KEY || '';
      const response = await fetch(`${apiUrl}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': modeApiKey,
        },
        body: JSON.stringify({ company_name: searchTerm }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        let errorMessage = 'Failed to fetch data. Ensure backend is running and API keys are set.';
        try {
            const errJSON = JSON.parse(errorText);
            if (errJSON && errJSON.detail) {
                errorMessage = String(errJSON.detail);
            }
        } catch (e) {
            // ignore JSON parse error
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      setCompanyData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={() => setIsAuthenticated(true)} />;
  }

  return (
    <div className="min-h-screen p-8 bg-slate-50 relative overflow-hidden">
      {/* Background decorative blobs */}
      <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-blue-400/20 rounded-full mix-blend-multiply filter blur-3xl opacity-50 -translate-x-1/2 -translate-y-1/2"></div>
      <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-indigo-400/20 rounded-full mix-blend-multiply filter blur-3xl opacity-50 translate-x-1/2 -translate-y-1/2"></div>

      <header className="mb-12 text-center relative z-10 pt-10">
        <div className="absolute top-6 right-6">
          <button
            onClick={handleLogout}
            className="px-6 py-2.5 bg-white text-slate-600 font-bold rounded-xl shadow-sm hover:text-red-600 hover:shadow-md transition-all ring-1 ring-slate-900/5"
          >
            Logout
          </button>
        </div>
        <h1 className="text-5xl font-black text-slate-800 mb-6 tracking-tight">
          Smart Company <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Intelligence</span> Engine
        </h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto font-medium">
          Enter a company name to get real-time insights, links, job postings, and reviews powered by AI.
        </p>
      </header>

      <main className="max-w-5xl mx-auto relative z-10">
        <form onSubmit={handleSearch} className="mb-16 flex justify-center shadow-2xl rounded-2xl max-w-2xl mx-auto ring-1 ring-slate-900/5">
          <input
            type="text"
            placeholder="Search any company... (e.g. Google, Airbnb)"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-8 py-5 text-xl bg-white border-0 rounded-l-2xl focus:outline-none text-slate-800 placeholder:text-slate-400 font-medium"
            required
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="px-10 py-5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-xl font-bold rounded-r-2xl hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Search'}
          </button>
        </form>

        {/* State rendering */}
        <div className="flex flex-col items-center">
          {loading && (
            <div className="flex flex-col items-center gap-4 text-slate-500 my-12 animate-pulse">
              <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
              <div className="font-semibold text-lg text-blue-600">Gathering intelligence from the web...</div>
            </div>
          )}

          {error && (
            <div className="w-full max-w-2xl bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl shadow-sm my-8 text-center font-medium">
              🚨 {error}
            </div>
          )}

          {!loading && !error && !companyData && (
            <div className="text-center text-slate-500 font-medium my-12 opacity-50">
              Ready to analyze companies in real-time.
            </div>
          )}

          {companyData && !loading && (
            <CompanyCard data={companyData} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
