# Smart Company Intelligence Engine

## Description
A comprehensive full-stack application that provides real-time insights, relevant links, job postings, and review snippets for any company using search engine integration and generative AI.

## Features
- Real-time intelligent search to fetch the most relevant links for a given company.
- Automated web scraping of search results for deeper company context.
- Generative AI synthesis to summarize findings concisely for the user.
- Responsive, modern UI with visually appealing aesthetics.
- Modular and scalable backend architecture.

## Tech Stack
### Frontend
- React
- Vite
- Tailwind CSS

### Backend
- Python & FastAPI
- Uvicorn
- BeautifulSoup4
- Google Search Results (SerpAPI)
- Google Generative AI (Gemini)

## Setup Instructions

### Environment Setup
You'll need `SERP_API_KEY` and `GEMINI_API_KEY` for the backend. Configure environment variables using the provided examples.

1. **Backend Configuration:**
    `cd backend`
    Copy `.env.example` to `.env` and fill out your keys.

2. **Frontend Configuration:**
    `cd frontend`
    Copy `.env.example` to `.env`. Leave as default (`VITE_API_URL=http://localhost:8000` for local dev or production URL for deployment).

### Local Development
1. **Start Backend Server:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Or `.\venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start Frontend Server:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Deployment Instructions

### Backend → Render / Railway
1. Push your repository to a platform like GitHub.
2. Connect the repository to your hosting service (e.g., Render or Railway).
3. Set the build command to `pip install -r backend/requirements.txt` (or configure via the given runtime).
4. Set the start command exactly to:
   ```bash
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. Add `SERP_API_KEY` and `GEMINI_API_KEY` in your platform's environment variables.

### Frontend → Vercel / Netlify
1. Connect your repository to Vercel or Netlify.
2. Set the root directory settings to `frontend` if deploying a monolithic repo.
3. The build command is `npm run build` and output directory is `dist`.
4. Add the `VITE_API_URL` environment variable containing the URL of your deployed backend (e.g., `https://my-backend-url.onrender.com`).
