import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SolGuild API"
    DEVNET_RPC_URLS: list[str] = [
        "https://api.devnet.solana.com",
        "https://rpc.ankr.com/solana_devnet",
    ]
    DEVNET_CLUSTER_PARAM: str = "?cluster=devnet"
    ESCROW_KEYPAIR_PATH: str = "escrow-keypair.json"
    DATABASE_URL: str = "sqlite:///./bounties.db"
    UPLOAD_DIR: str = "./uploads"
    FIXTURES_DIR: str = "../fixtures"
    DEFAULT_REWARD_SOL: float = 0.01
    MAX_GEOFENCE_METERS: int = 150
    CLAIM_TIMEOUT_MINUTES: int = 10
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.FIXTURES_DIR, exist_ok=True)
