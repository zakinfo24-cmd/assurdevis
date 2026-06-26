# AssurDevis — Deployment Guide

## Overview
AssurDevis is a FastAPI-based insurance quote assistant for Algerian insurance products. It uses Groq AI for conversational responses and supports PDF contract analysis.

## Requirements

### System Dependencies
- Python 3.10+
- (Optional) Tesseract OCR for PDF scanning: `apt-get install tesseract-ocr`
- (Optional) PyMuPDF for PDF text extraction

### Python Dependencies
See `requirements.txt`:
- FastAPI 0.138.0
- Uvicorn 0.49.0
- Pydantic 2.13.4
- httpx 0.28.1
- python-dotenv 1.2.2
- PyMuPDF 1.27.2.3 (PDF extraction)
- Pillow 12.2.0 (Image processing)
- pytesseract 0.3.13 (OCR)

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required
GROQ_API_KEY=your_groq_api_key

# Optional (for key rotation)
GROQ_API_KEY_2=
GROQ_API_KEY_3=
GROQ_API_KEY_4=
GROQ_API_KEY_5=

# Optional (for email exports)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
SMTP_FROM=noreply@assurdevis.com
EXPORT_TO_EMAILS=admin@example.com

# CORS (default: allow all)
ALLOWED_ORIGINS=*
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Access at http://localhost:8000
```

## Railway Deployment

### 1. Connect GitHub Repository
- Push code to GitHub
- Connect repo to Railway project

### 2. Configure Environment Variables
In Railway dashboard:
- Add `GROQ_API_KEY` and other required variables
- Set `ALLOWED_ORIGINS` if needed

### 3. Build Configuration
Railway uses `railway.toml`:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### 4. Deploy
- Push to main branch
- Railway auto-deploys
- Access at `https://assurdevis-production.up.railway.app`

## API Endpoints

### Public
- `GET /` — Serve index.html (web interface)
- `GET /health` — Health check
- `POST /init` — Initialize conversation
- `POST /chat` — Chat with AI assistant
- `POST /devis/auto` — Calculate auto insurance quote
- `POST /devis/rd` — Calculate other insurance quote
- `POST /analyse` — Analyze insurance contract
- `POST /rating` — Submit quote rating
- `GET /rating/stats` — Get rating statistics

### Admin
- `GET /admin/stats` — Get statistics
- `GET /admin/export/download` — Download JSON export
- `GET /admin/export/download/csv` — Download CSV export
- `GET /admin/report` — Get HTML report
- `POST /admin/export/mail` — Send export by email

## Troubleshooting

### "index.html not found"
- Ensure `static/index.html` exists
- Check file permissions
- Verify `STATIC` path in main.py

### Groq API errors
- Verify `GROQ_API_KEY` is valid
- Check rate limits (429 errors trigger key rotation)
- Ensure network connectivity

### PDF extraction fails
- Install Tesseract: `apt-get install tesseract-ocr`
- Verify PyMuPDF is installed: `pip install PyMuPDF`
- Check file size (max 50 MB)

### Email export not working
- Verify SMTP credentials
- Check firewall/network access to SMTP server
- Enable "Less secure apps" for Gmail

## Performance Notes

- Conversations stored in memory (lost on restart)
- Knowledge base loaded at startup
- Groq API calls cached per conversation
- Static files served via FastAPI StaticFiles

## Security Considerations

- CORS open by default (configure `ALLOWED_ORIGINS` in production)
- No authentication on public endpoints
- Rate limiting recommended for production
- Sensitive data (API keys) in environment variables only

## Monitoring

Check logs via Railway dashboard:
- Build logs: Deployment process
- Deploy logs: Runtime errors
- HTTP logs: Request/response analysis

Health endpoint: `GET /health`
```json
{
  "status": "ok",
  "groq": true,
  "model": "llama-3.3-70b-versatile",
  "keys_loaded": 1,
  "active_key": 1,
  "version": "3.0"
}
```

## Support

For issues:
1. Check logs in Railway dashboard
2. Verify environment variables
3. Test health endpoint
4. Review error messages in deploy logs

