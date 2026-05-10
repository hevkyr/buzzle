--[[
  buzzle/lua/buzzle.lua
  Lightweight Lua wrapper for the buzzle API.

  Requirements:
    luarocks install luasocket

  Usage:
    lua buzzle.lua          -- one phrase
    lua buzzle.lua 5        -- five phrases
    lua buzzle.lua 1 42     -- one phrase, seed=42
--]]

local http = require("socket.http")
local json_ok, json = pcall(require, "cjson")
if not json_ok then
  -- fallback: basic JSON decode for simple cases
  json = {
    decode = function(s)
      -- Very minimal decoder for our response shape
      local t = {}
      s:gsub('"([^"]+)"%s*:%s*"([^"]*)"', function(k, v) t[k] = v end)
      s:gsub('"([^"]+)"%s*:%s*(%d+)', function(k, v) t[k] = tonumber(v) end)
      return t
    end
  }
end

-- ── Config ────────────────────────────────────────────────────────────────────

local API_BASE = os.getenv("BUZZLE_API") or "http://localhost:8000"

-- ── Helpers ───────────────────────────────────────────────────────────────────

local function fetch(url)
  local body, status = http.request(url)
  if not body or status ~= 200 then
    io.stderr:write(string.format("✗ HTTP error %s fetching %s\n", tostring(status), url))
    os.exit(1)
  end
  return body
end

local function stars(score)
  local full = math.floor(score / 20)
  local s = ""
  for i = 1, 5 do
    s = s .. (i <= full and "★" or "☆")
  end
  return s
end

local function print_phrase(phrase, score, category, index)
  local n = index or 1
  print(string.format("\n  %d. \27[1;36m%s\27[0m", n, phrase))
  print(string.format("     %s  \27[2m[%s · score: %d/100]\27[0m", stars(score), category, score))
end

-- ── Main ──────────────────────────────────────────────────────────────────────

local count = tonumber(arg[1]) or 1
local seed  = arg[2] and ("&seed=" .. arg[2]) or ""

print("\n  \27[1mbuzzle\27[0m · lua wrapper")
print("  ──────────────────────")

if count == 1 then
  local url  = API_BASE .. "/phrase?count=1" .. seed
  local body = fetch(url)
  local data = json.decode(body)
  print_phrase(data.phrase, data.score, data.category, 1)
else
  -- Parse array response
  local url  = API_BASE .. string.format("/phrase?count=%d%s", count, seed)
  local body = fetch(url)

  -- Extract each phrase block (works with cjson or manual parsing)
  local i = 0
  for block in body:gmatch("{[^}]+}") do
    i = i + 1
    local d = json.decode("{" .. block:match("{(.+)}") .. "}")
    if d and d.phrase then
      print_phrase(d.phrase, d.score or 0, d.category or "?", i)
    end
  end
end

print()
