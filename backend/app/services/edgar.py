import requests
from typing import Optional

HEADERS = {"User-Agent": "EarningsSignalExtractor research@example.com"}
DEMO_TRANSCRIPTS = {
    "AAPL": "We are extremely pleased to report another record quarter. Revenue came in at $89.5 billion, up 8% year over year. Our services business continues to accelerate and we are raising our guidance for the next quarter. We feel very confident about our product pipeline and the opportunities ahead. iPhone demand remains robust across all geographies. We expect continued momentum and are raising our full-year outlook significantly.",
    "META": "Thank you for joining us. This quarter we faced significant headwinds from the macroeconomic environment. Revenue was $28.1 billion, which while growing, came in below some expectations. We want to be transparent about the challenges ahead. We are carefully monitoring ad spend trends and may need to adjust our investment plans if conditions deteriorate. We remain cautiously optimistic but want to acknowledge the uncertainty in the current environment.",
    "MSFT": "We delivered another strong quarter with revenue of $56.5 billion. Our cloud business Azure grew 29% and we are seeing tremendous demand for our AI services. We are raising our guidance and feel very confident in our competitive positioning. The integration of AI across our product suite is proceeding ahead of schedule and customer feedback has been overwhelmingly positive. We see a long runway of growth ahead.",
    "GOOGL": "Revenue for the quarter was $76.7 billion, reflecting growth across search and cloud. While we are pleased with these results, we want to acknowledge that the advertising market continues to show some softness. We are being disciplined about costs and will continue to invest in AI capabilities. Our guidance for next quarter reflects both the opportunities we see and the uncertainties that remain in the broader economy.",
    "NVDA": "This was a historic quarter for NVIDIA. Revenue reached $22.1 billion, up 122% year over year. Demand for our data center products has exceeded our most optimistic projections. We are raising guidance significantly and expect this momentum to continue. Every major cloud provider and AI company is deploying our infrastructure. We are in the very early stages of what we believe will be a multi-decade AI infrastructure build-out.",
}

def fetch_transcript(ticker: str, quarter: str = "Q1", year: int = 2024) -> Optional[str]:
    ticker = ticker.upper()
    return DEMO_TRANSCRIPTS.get(ticker, DEMO_TRANSCRIPTS["AAPL"])

def get_company_name(ticker: str) -> str:
    names = {"AAPL": "Apple Inc.", "META": "Meta Platforms", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.", "NVDA": "NVIDIA Corp.", "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc."}
    return names.get(ticker.upper(), ticker.upper())
