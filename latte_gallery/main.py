import uvicorn

from latte_gallery.core.setup import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
