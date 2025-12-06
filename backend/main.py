import os
from app.api import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5328"))
    app.run(host="0.0.0.0", port=port)
