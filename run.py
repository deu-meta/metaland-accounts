import uvicorn
from dotenv import load_dotenv

load_dotenv(verbose=True)

if __name__ == "__main__":
    uvicorn.run("mtl_accounts.main:app", host="0.0.0.0", port=8000, reload=True)
