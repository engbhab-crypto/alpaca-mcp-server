import os

import httpx
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Alpaca SIP Read-Only API")


@app.get("/")
async def root():
    return {"status": "ok", "service": "alpaca-sip-read-only"}


@app.get("/snapshot/{symbol}")
async def snapshot(
    symbol: str,
    feed: str = Query(default="sip"),
):
    api_key = os.environ.get("ALPACA_API_KEY")
    secret_key = os.environ.get("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        raise HTTPException(status_code=500, detail="Alpaca credentials are not configured")

    symbol = symbol.upper().strip()

    url = f"https://data.alpaca.markets/v2/stocks/{symbol}/snapshot"

    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key,
    }

    params = {"feed": feed}

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return response.json()
