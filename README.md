# 🌀 buzzle

> **The world's most over-engineered motivational phrase generator.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Go](https://img.shields.io/badge/Go-1.22+-00ADD8?style=flat-square&logo=go&logoColor=white)](https://golang.org)
[![Lua](https://img.shields.io/badge/Lua-5.4-2C2D72?style=flat-square&logo=lua&logoColor=white)](https://lua.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 🤔 What is buzzle?

**buzzle** is a ridiculously serious project that generates absurd motivational phrases by combining random nouns, verbs, and adjectives in ways that sound profound but mean absolutely nothing.

```
"The disciplined cactus never apologizes to gravity."
"Hustle harder than your neighbor's WiFi password."
"A confused penguin still knows its CSV encoding."
```

It does this via:
- 🐍 **Python** — REST API (FastAPI) with phrase generation engine
- 🐹 **Go** — blazing-fast CLI client
- 🌙 **Lua** — lightweight scripting wrapper
- 🐳 **Docker** — one-command deploy
- 🌐 **HTML/JS** — interactive web frontend
- ✅ **pytest** — full test coverage
- 🔄 **GitHub Actions** — CI/CD pipeline

---

## 📁 Project Structure

```
buzzle/
├── api/                    # Python FastAPI backend
│   ├── main.py             #   → REST endpoints
│   ├── engine.py           #   → phrase generation logic
│   ├── words.py            #   → word banks (nouns, verbs, adjectives)
│   └── requirements.txt    #   → dependencies
├── cli/                    # Go CLI client
│   ├── main.go             #   → CLI logic
│   └── go.mod              #   → Go module
├── lua/                    # Lua wrapper
│   └── buzzle.lua          #   → HTTP client + formatter
├── tests/                  # pytest test suite
│   ├── test_engine.py      #   → unit tests
│   └── test_api.py         #   → integration tests
├── docs/                   # Documentation
│   └── index.html          #   → interactive web UI
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-service compose
├── .github/workflows/      # CI/CD
│   └── ci.yml              #   → test + build pipeline
└── README.md               # You are here
```

---

## 🚀 Quick Start

### Option 1 — Docker (recommended)

```bash
git clone https://github.com/hevkyr/buzzle
cd buzzle
docker compose up
```

API live at `http://localhost:8000` · Docs at `http://localhost:8000/docs`

### Option 2 — Python only

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

### Option 3 — Go CLI

```bash
cd cli
go build -o buzzle .
./buzzle generate
./buzzle generate --count 5
./buzzle generate --json
```

### Option 4 — Lua script

```bash
lua lua/buzzle.lua
lua lua/buzzle.lua 3   # generate 3 phrases
```

---

## 🌐 API Reference

### `GET /phrase`

Generate a single motivational phrase.

```bash
curl http://localhost:8000/phrase
```

```json
{
  "phrase": "The disciplined cactus never apologizes to gravity.",
  "score": 87,
  "category": "hustle",
  "generated_at": "2026-05-10T12:00:00Z"
}
```

### `GET /phrase?count=N`

Generate N phrases (max 20).

```bash
curl "http://localhost:8000/phrase?count=5"
```

### `GET /phrase/rated`

Get a phrase with a "profoundness score" (completely made up).

### `GET /stats`

API usage statistics.

```json
{
  "total_phrases_generated": 1337,
  "uptime_seconds": 42069,
  "most_used_noun": "cactus",
  "engine_version": "1.0.0"
}
```

### `POST /phrase/custom`

Build a phrase with your own words.

```bash
curl -X POST http://localhost:8000/phrase/custom \
  -H "Content-Type: application/json" \
  -d '{"noun": "developer", "verb": "refactor", "adjective": "caffeinated"}'
```

---

## 🧪 Tests

```bash
cd tests
pip install -r ../api/requirements.txt pytest httpx
pytest -v
```

Expected output:
```
tests/test_engine.py::test_phrase_is_string PASSED
tests/test_engine.py::test_phrase_not_empty PASSED
tests/test_engine.py::test_score_range PASSED
tests/test_engine.py::test_custom_phrase PASSED
tests/test_api.py::test_get_phrase PASSED
tests/test_api.py::test_get_multiple_phrases PASSED
tests/test_api.py::test_stats_endpoint PASSED
tests/test_api.py::test_custom_phrase_endpoint PASSED

8 passed in 0.42s
```

---

## 🧠 How the Engine Works

The phrase generator uses a **Markov-inspired template system** with 4 base templates:

```
Template A: "The {adj} {noun} never {verb} {preposition} {noun2}."
Template B: "{verb} harder than your {noun}'s {noun2}."
Template C: "A {adj} {noun} still knows its {noun2} encoding."
Template D: "Never let a {adj} {noun} {verb} your {noun2}."
```

Words are selected from banks of 100+ nouns, 80+ verbs, and 60+ adjectives, with a seeded PRNG to ensure reproducibility when needed.

The **profoundness score** is calculated as:
```
score = (syllable_count × 12) + (word_length_avg × 7) + random_noise
```
(It's fake. But it feels real.)

---

## 🐳 Docker Details

```yaml
# docker-compose.yml spins up:
# - buzzle-api  → FastAPI on :8000
# - buzzle-web  → Nginx serving the frontend on :80
```

```bash
docker compose up -d          # start detached
docker compose logs -f        # follow logs
docker compose down           # stop everything
```

---

## 🌙 Lua Usage

The Lua wrapper requires `luasocket` for HTTP:

```bash
luarocks install luasocket
lua lua/buzzle.lua            # one phrase
lua lua/buzzle.lua 10         # ten phrases
```

---

## 🤝 Contributing

1. Fork it
2. Create a branch: `git checkout -b feat/more-absurdity`
3. Add words to `api/words.py` — the weirder the better
4. Run tests: `pytest tests/ -v`
5. Open a PR

---

## 📄 License

MIT — do whatever you want, just keep the cactus.

---

<div align="center">
  <sub>Built with excessive seriousness by <a href="https://github.com/hevkyr">hevkyr</a> · 🇧🇷</sub>
</div>
