import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="ScamSentry", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

class Message(BaseModel):
    text: str = Field(min_length=1, max_length=10000)

RULES = [
    (r"\b(urgent|immediately|act now|final warning)\b", 15, "Urgency or pressure"),
    (r"\b(gift card|wire transfer|bitcoin|payment required)\b", 25, "Risky payment request"),
    (r"\b(password|verification code|social security number)\b", 25, "Sensitive information request"),
    (r"\b(account suspended|locked account|verify your account)\b", 20, "Account problem claim"),
    (r"\b(click (?:this |the )?link|visit this link)\b", 15, "Pressure to follow a link"),
    (r"\b(prize|lottery|inheritance)\b", 15, "Unexpected reward"),
    (r"https?://[^\s]+", 10, "Contains a link; verify independently"),
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(message: Message):
    findings = [{"reason": reason, "points": points} for pattern, points, reason in RULES if re.search(pattern, message.text, re.IGNORECASE)]
    score = min(100, sum(f["points"] for f in findings))
    level = "high" if score >= 60 else "medium" if score >= 25 else "low"
    recommendation = ("Do not reply, click, or send money. Verify using a trusted contact method." if level == "high" else
                      "Verify the sender independently before acting." if level == "medium" else
                      "No strong rule matches. This does not establish that the message is safe.")
    return {"risk_score": score, "risk_level": level, "findings": findings, "recommendation": recommendation,
            "disclaimer": "Uncalibrated heuristic score, not a probability. False positives and missed scams are possible."}
