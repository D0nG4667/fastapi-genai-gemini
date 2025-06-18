# FastAPI Gemini AI Server

This project showcases the implementation of a FastAPI-based API server tailored for AI applications, utilizing the Gemini model as its core inference engine.

---

## Features

- **JWT Authentication**: Secure endpoints using OAuth2 password flow and JWT tokens.
- **Google Gemini Integration**: Use Gemini for text generation via a simple API.
- **Rate Limiting**: Prevent abuse with configurable per-user and global rate limits.
- **Extensible AI Platform**: Easily swap or extend AI backends.
- **Environment-based Configuration**: Securely manage secrets and settings.
- **Pydantic Models**: Robust request/response validation.

---

## Project Structure

src/
├── main.py               # FastAPI app and API routes

├── ai/
│   ├── base.py           # Abstract AI platform interface
│   └── gemini.py         # The concrete implementation of the AIPlatform interface for Gemini.

├── auth/
│   ├── auth.py           # JWT auth, token creation, user extraction
│   └── throttling.py     # Provides a simple in-memory rate limiter with different limits for authenticated and unauthenticated users.

├── schemas/
│   └── pydantic.py       # Pydantic models for requests/responses

├── prompts/
│   └── system_prompt.md  # The System prompt for the AI

---

## Getting Started

### Prerequisites

- Python 3.10+
- [Google Gemini API Key](https://ai.google.dev/)
- [uv](https://github.com/uv-mamba/uv) (for fast installs)

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/fastapi-genai-gemini.git
   cd fastapi-genai-gemini
    ```

2. **Install dependencies**
    Ensure you have `uv` installed for fast dependency management:

   ```sh
   uv pip install -r pyproject.toml
   ```

3. **Set environment variables**
   Create a `.env` file in the root directory with your Google Gemini API key:

   ```env
    GEMINI_API_KEY=your_gemini_api_key
    JWT_SECRET_KEY=your_jwt_secret_key
    JWT_ALGORITHM=HS256
   ```

4. **Run the server**
   Start the FastAPI server using uvicorn:

   ```sh
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the API**
   Open your browser and navigate to `http://localhost:8000/docs` to view the interactive API documentation.

---

### Endpoints

| Method | Path           | Description                        | Auth Required |
|--------|----------------|------------------------------------|--------------|
| GET    | `/`            | Welcome message                    | No           |
| POST   | `/token`       | Obtain JWT token                   | No           |
| GET    | `/users/me`    | Get current user info              | Yes          |
| GET    | `/model_info`  | Get Gemini model info              | No           |
| POST   | `/chat`        | Generate AI response from Gemini   | Optional     |

---

## Customization

- **System Prompt**: Edit `system_prompt.md` to change the AI's behavior.
- **Rate Limits**: Adjust values in `throttling.py`.
- **AI Model**: Change the Gemini model in `gemini.py`.

---

## Security Notes

- Never commit your real API keys or secrets.
- Use strong, unique values for `JWT_SECRET_KEY`.
- For production, set `DEBUG=False` and use HTTPS.

---

## 👥 Authors

🕺🏻**Gabriel Okundaye**

- GitHub: [GitHub Profile](https://github.com/D0nG4667)

- LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/dr-gabriel-okundaye)

## ⭐️ Show your support

If you like this project kindly show some love, give it a 🌟 **STAR** 🌟. Thank you!

## 📝 License

This project is [MIT](/LICENSE) licensed.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini](https://ai.google.dev/)
- [Pydantic](https://docs.pydantic.dev/)
- [python-jose](https://python-jose.readthedocs.io/)

---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.