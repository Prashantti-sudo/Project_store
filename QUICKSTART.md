# Quick Start Guide

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- API keys for at least one LLM provider (OpenAI, Anthropic, or Google)

## Quick Setup

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy env.example .env  # Windows
# OR
cp env.example .env    # macOS/Linux

# Edit .env and add your API keys
# At minimum, set PRIMARY_LLM_PROVIDER and one API key

# Run backend
python main.py
```

Backend will start on `http://localhost:8000`

### 2. Frontend Setup (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start on `http://localhost:3000`

## Using the Application

1. Open `http://localhost:3000` in your browser
2. Choose a workflow:
   - **Image Upload → Motion Effect**: Upload an image to generate motion effects
   - **Product URL → AI Ad Image**: Enter a product URL to generate ad creatives

## API Key Setup

### Minimum Required Configuration

Edit `backend/.env`:

```env
PRIMARY_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

### Optional (for image generation)

```env
IMAGE_GENERATION_PROVIDER=openai
# Uses OPENAI_API_KEY for DALL-E

# OR use Stability AI
IMAGE_GENERATION_PROVIDER=stability
IMAGE_GENERATION_API_KEY=your-stability-key

# OR use Replicate
IMAGE_GENERATION_PROVIDER=replicate
IMAGE_GENERATION_API_KEY=your-replicate-key
```

### Optional (for motion effects)

```env
MOTION_EFFECT_PROVIDER=stability
MOTION_EFFECT_API_KEY=your-key-here
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (needs 3.9+)
- Verify virtual environment is activated
- Check `.env` file exists and has required keys

### Frontend won't start
- Check Node.js version: `node --version` (needs 18+)
- Delete `node_modules` and run `npm install` again

### API errors
- Verify API keys are correct in `.env`
- Check API key has sufficient credits/permissions
- Review backend console for detailed error messages

### CORS errors
- Ensure backend is running on port 8000
- Check `ALLOWED_ORIGINS` in `.env` includes `http://localhost:3000`

## Production Build

### Frontend
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```




