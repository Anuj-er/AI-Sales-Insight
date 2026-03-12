# API Documentation

## Authentication
All API endpoints under the `/api/` route require an API key to be passed in the headers.
- **Header Key:** `X-API-Key`
- **Value:** The secret key defined in the `.env` file (`API_KEY`).

---

## Endpoints

### 1. File Upload & Processing
**Endpoint:** `POST /api/upload`

**Description:**
Accepts a data file (CSV or Excel) and an email address. The endpoint parses the data, utilizes the Groq LLM to generate a professional executive summary narrative, and dispatches the styled HTML report to the provided email address.

**Content-Type:** `multipart/form-data`

**Request Body:**
| Key | Type | Description | Required |
| --- | --- | --- | --- |
| `file` | File | The sales data file (`.csv` or `.xlsx`). | Yes |
| `email` | String | The recipient's email address. | Yes |

**Success Response (200 OK):**
```json
{
  "message": "Sales summary successfully generated and sent to target@example.com."
}
```

**Error Responses:**
- `400 Bad Request`: Missing file/email, or invalid file format.
- `401 Unauthorized`: Missing or invalid `X-API-Key`.
- `422 Unprocessable Entity`: Data parsing failure or invalid email format.
- `429 Too Many Requests`: Rate limit exceeded (5 requests per hour per IP).
- `500 Internal Server Error`: LLM generation failure or email delivery failure.

---

## API Access

- **Local Development:** `http://localhost:8000/docs`
- **Production (Hugging Face Space):** `https://anuj-er-sales-insight.hf.space/docs`

For interactive testing and automatic schema definitions, access the Swagger UI at the `/docs` endpoint of your deployed backend.
