# Face Comparison from URLs

This simple Flask-based API allows you to compare faces from two images using their URLs. Powered by DeepFace, it quickly checks if the faces match.

## Features
- **Face Comparison**: Compare two images using just URLs.
- **Powered by DeepFace**: Accurate face verification.
- **Easy to Use**: No base64 encoding required, just provide image URLs.

## How It Works
1. Send a POST request with two image URLs (`base_image` and `comparison_image`).
2. The API compares the faces and returns whether they match (`verified`) and their similarity (`distance`).

## Endpoint & Request Example
`POST /verify`

### Request Body Example
```json
{
  "base_image": "https://example.com/image1.jpg",
  "comparison_image": "https://example.com/image2.jpg"
}
```

### Response Example
```json
{
  "verified": true,
  "distance": 0.22
}
```

## Why Use This?
- Quick and easy face comparison via URLs.
- No need for complex setup or base64 encoding.
- Ideal for security and face recognition projects.

### Get Started
1. Clone the repo.
2. Install dependencies.
3. Run the Flask app and make requests to `/verify`.
