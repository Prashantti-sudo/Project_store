# AI Ad Creative Generator

A premium AI-powered platform for generating professional ad creatives with two main workflows:

1. **Image Upload → Motion Effect Generation**: Upload an image and generate stunning motion effects
2. **Product URL → AI Ad Image Generator**: Enter a product URL and automatically generate professional ad creatives in multiple platform sizes

## 🎨 Design Philosophy

This application features a **premium SaaS design** inspired by Stripe, Linear, and Notion:
- Clean, minimal interface with professional color palette
- Smooth Framer Motion transitions and animations
- Modern typography with Inter font family
- Skeleton loaders for better loading states
- Clear progress indicators throughout
- Fully responsive design (Desktop, Tablet, Mobile)

## Tech Stack

### Frontend
- React.js (JavaScript)
- Vite
- Tailwind CSS
- Framer Motion
- Axios
- Fully responsive (Desktop, Tablet, Mobile)

### Backend
- Python FastAPI
- REST APIs
- Environment variables for configuration
- Clean folder structure

### AI/ML
- LLM (OpenAI / Claude / Gemini) for:
  - Image understanding
  - Category classification
  - Text/keyword generation
- Image Generation/Animation APIs for:
  - Motion effects
  - Ad creative generation

## Project Structure

```
.
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── WorkflowSelector.jsx
│   │   │   ├── ImageUploadWorkflow.jsx
│   │   │   └── ProductURLWorkflow.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── backend/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   ├── image_service.py
│   │   ├── motion_service.py
│   │   └── product_scraper.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## 📁 Project Structure

```
.
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── WorkflowSelector.jsx
│   │   │   ├── ImageUploadWorkflow.jsx
│   │   │   ├── ProductURLWorkflow.jsx
│   │   │   └── SkeletonLoader.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── backend/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   ├── image_service.py
│   │   ├── motion_service.py
│   │   └── product_scraper.py
│   ├── main.py
│   ├── requirements.txt
│   └── env.example
├── .env.example
├── README.md
└── QUICKSTART.md
```

## 🚀 Setup Instructions

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- API keys for at least one LLM provider (OpenAI, Anthropic, or Google)

### Backend Setup

1. **Navigate to the backend directory:**
```bash
cd backend
```

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**
   - **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   - **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Create a `.env` file:**
   - **Windows:**
   ```bash
   copy env.example .env
   ```
   - **macOS/Linux:**
   ```bash
   cp env.example .env
   ```

6. **Edit `.env` and add your API keys:**
```env
# Required: At least one LLM provider
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
PRIMARY_LLM_PROVIDER=openai

# Optional: Image generation
IMAGE_GENERATION_API_KEY=your_image_generation_api_key
IMAGE_GENERATION_PROVIDER=stability

# Optional: Motion effects
MOTION_EFFECT_API_KEY=your_motion_effect_api_key
MOTION_EFFECT_PROVIDER=stability

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

7. **Run the backend server:**
```bash
python main.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

### Quick Start (Both Servers)

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:3000` in your browser.

## API Endpoints

### Health Check
- `GET /health` - Check API status

### Motion Effect Generation
- `POST /api/generate-motion-effect`
  - Body: `multipart/form-data` with `image` file
  - Returns: Motion effect URL, analysis, keywords

### Ad Creative Generation
- `POST /api/generate-ad-from-url`
  - Body: `{"product_url": "https://example.com/product"}`
  - Returns: Generated ad images, product info, keywords, captions

## Features

### Image Upload Workflow
- Drag & drop or click to upload images
- Real-time preview
- AI-powered image analysis
- Motion effect generation
- Download results

### Product URL Workflow
- Automatic product information extraction
- AI-powered category classification
- Multiple ad creative variations
- Generated keywords and captions
- Professional ad designs

## 🔑 Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `PRIMARY_LLM_PROVIDER` | Primary LLM provider | `openai`, `anthropic`, or `google` |

**Note:** At least one LLM API key is required (see below)

### LLM Provider Variables (Choose at least one)

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 and DALL-E | Optional* |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | Optional* |
| `GOOGLE_API_KEY` | Google API key for Gemini | Optional* |

*At least one LLM API key is required

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `IMAGE_GENERATION_API_KEY` | API key for image generation | - |
| `IMAGE_GENERATION_PROVIDER` | Image generation provider (`stability`, `openai`, `replicate`) | `stability` |
| `MOTION_EFFECT_API_KEY` | API key for motion effects | - |
| `MOTION_EFFECT_PROVIDER` | Motion effect provider (`stability`, `runway`, `replicate`) | `stability` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000,http://localhost:5173` |

### Example `.env` File

```env
# Minimum required configuration
PRIMARY_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# Optional: For image generation
IMAGE_GENERATION_PROVIDER=openai
# Uses OPENAI_API_KEY for DALL-E

# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Development

### Frontend Development
- Hot reload enabled
- Proxy configured for API calls
- Responsive design with Tailwind CSS
- Smooth animations with Framer Motion

### Backend Development
- Auto-reload on code changes (when DEBUG=True)
- CORS configured for frontend
- Error handling and logging
- Modular service architecture

## 🏗️ Production Build

### Frontend

1. **Build for production:**
```bash
cd frontend
npm run build
```

2. **Preview production build:**
```bash
npm run preview
```

The built files will be in `frontend/dist/`

### Backend

For production, use a production ASGI server:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or with Gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 Run Instructions

### Development Mode

**Backend:**
```bash
cd backend
python main.py
# Runs on http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

### Production Mode

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the dist/ folder with a static file server
```

## 🐛 Troubleshooting

### Backend Issues

- **Port already in use:** Change `PORT` in `.env` or kill the process using port 8000
- **Module not found:** Ensure virtual environment is activated and dependencies are installed
- **API key errors:** Verify your API keys are correct in `.env`

### Frontend Issues

- **Port already in use:** Change port in `vite.config.js` or kill the process using port 3000
- **Build errors:** Delete `node_modules` and run `npm install` again
- **CORS errors:** Ensure backend is running and `ALLOWED_ORIGINS` includes your frontend URL

### Common Issues

- **"Could not extract product information":** The product URL may not be accessible or may require authentication
- **Image generation fails:** Check your image generation API key and provider settings
- **Slow responses:** AI processing can take 10-30 seconds depending on the provider

## License

MIT License

## Support

For issues and questions, please open an issue on the repository.

