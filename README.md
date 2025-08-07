# Project Overview

Lang Cards is a language learning app backend built with FastAPI. It creates AI-generated vocabulary cards with images and context using Gemini models.

A witty aspect of the project is its efficient handling of image reuse across different languages. For example, words like "cat" / "貓" / "кіт" share the same concept—and thus the same image—helping reduce unnecessary image generation costs while preserving multilingual relevance and consistency.

This project adheres to the recommended practices from the [FastAPI Best Practices Guide](https://github.com/zhanymkanov/fastapi-best-practices).

-----
Tech Stack

    Backend: FastAPI, SQLAlchemy
    
    LLM: Mirascope, Gemini

    Database: PostgreSQL

    Storage & Backend Services: Supabase

    Frontend: React Native
-----

-----
Requirements

    Python 3.10+

    A Supabase account

    A Supabase storage bucket (for storing and serving word images)

    Your own Google API key for Gemini models

    Create a .env file in the project root as specified in env.example

-----

-----

## Running the Application

To start the development server:

```bash
uv run uvicorn src.main:app --reload
```
-----

## API Documentation

Once your application is running, you can access Swagger UI in your web browser. Just open your browser and go to the `/docs` endpoint:

[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

-----