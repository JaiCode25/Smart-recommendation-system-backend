# Smart Recommendation System — API Documentation

Base URL (local development): `http://127.0.0.1:8000`

All endpoints are prefixed with `/api`.

Full interactive docs (auto-generated): `http://127.0.0.1:8000/docs`

---

## 1. Get Items

```
GET /api/items
```

Returns a list of content items (YouTube, Instagram, Shopping, News, etc.)

**Query Parameters (all optional):**

| Param | Type | Description |
|---|---|---|
| source | string | Filter by source: `youtube`, `instagram`, `shopping`, `demo` |
| category | string | Filter by category |
| tag | string | Filter by a specific tag |
| query | string | Keyword search across title/description |
| limit | integer | Max results (default 50, max 200) |
| offset | integer | Pagination offset (default 0) |

**Example:**
```
GET /api/items?source=youtube&limit=10
```

**Sample Response:**
```json
[
  {
    "id": 6,
    "item_id": "yt-prog-001",
    "source": "demo",
    "title": "Python 3.14 Full Course",
    "description": "...",
    "url": "https://youtube.com/...",
    "thumbnail": "https://...",
    "category": "programming",
    "creator_or_brand": "Core Code Academy",
    "price": null,
    "tags": ["python", "programming", "technology"],
    "metadata": { "views": 1850000, "rating": 4.9 },
    "created_at": "2026-08-26T18:20:42.83"
  }
]
```

---

## 2. Get Single Item

```
GET /api/items/{id}
```

Returns full detail for one item by its database `id`.

**Example:** `GET /api/items/6`

Returns `404` if the item does not exist.

---

## 3. Get Recommendations

```
GET /api/recommendations
```

Returns a ranked, personalized list of recommended items for a user, with score and explanation.

**Query Parameters:**

| Param | Type | Description |
|---|---|---|
| user_id | integer | **Required.** Target user (default 1) |
| limit | integer | Number of recommendations (default 12, max 50) |
| source_filter | string | Optional filter by source |
| category_filter | string | Optional filter by category |
| include_consumed | boolean | Include items the user already interacted with (default false) |

**Example:**
```
GET /api/recommendations?user_id=1&limit=10
```

**Sample Response (trimmed):**
```json
{
  "user_id": 1,
  "recommendations_count": 12,
  "generated_at": "2026-08-28T12:33:21",
  "recommendations": [
    {
      "item": { "id": 2, "title": "Top 10 Fast Bowling Spells...", "tags": ["cricket","sports"], "...": "..." },
      "score": 80.19,
      "rank": 1,
      "confidence_percentage": 80.2,
      "explanation": {
        "summary": "Direct match with your interests in 'cricket', 'sports'",
        "direct_matching_tags": ["cricket", "sports"],
        "expanded_matching_tags": ["bowling", "fast-bowling"]
      }
    }
  ]
}
```

> Note: This is a **query parameter** (`?user_id=1`), not a path parameter (`/recommendations/1`).

---

## 4. Record an Interaction (Like/View/Dislike/etc.)

```
POST /api/interactions
```

Logs a user action on an item. This is what makes recommendations update dynamically — after this call, future `GET /api/recommendations` calls for the same user will reflect the new interest.

**Request Body:**
```json
{
  "user_id": 1,
  "item_id": 6,
  "interaction_type": "like"
}
```

> ⚠️ The field is `interaction_type`, **not** `action`. Valid values: `view`, `click`, `like`, `dislike`, `save`, `skip`, `search`.

**Important:** `user_id` must already exist in the database (seeded users only, e.g. `user_id: 1`). Sending a non-existent `user_id` now correctly returns a `404` error (this was a bug we found and fixed).

**Sample Response:**
```json
{
  "id": 10,
  "user_id": 1,
  "item_id": 6,
  "item_title": "Python 3.14 Full Course",
  "item_source": "demo",
  "interaction_type": "like",
  "weight": 5,
  "timestamp": "2026-08-29T07:54:30.8"
}
```

---

## Typical Frontend Flow

1. Load home feed → `GET /api/recommendations?user_id=1`
2. User clicks Like → `POST /api/interactions` with `interaction_type: "like"`
3. Refresh feed → `GET /api/recommendations?user_id=1` again → order/scores will have changed

---

## CORS Note

The backend allows cross-origin requests via `CORSMiddleware`. If your frontend runs on a specific port (e.g. `localhost:5500`, `localhost:5173`), that origin needs to be present in `CORS_ORIGINS` in `app/config.py` on the backend — let the backend owner know your dev server's URL/port so it can be added.

---

## Known Notes / Gotchas

- `interaction_type` is the correct field name for interactions (not `action`).
- `user_id` in recommendations/interactions is a **query param**, not a URL path segment.
- Only seeded users exist right now (e.g. `user_id: 1`) — a non-existent user_id will return a 404.
