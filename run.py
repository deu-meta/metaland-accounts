import uvicorn
from dotenv import load_dotenv

from mtl_accounts.main import app

load_dotenv(verbose=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
