import asyncio, os, threading, functools, http.server, socketserver

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = "/workspace/.cache/ms-playwright/chromium_headless_shell-1255/chrome-headless-shell-linux64/chrome-headless-shell"
PORT = 8791


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    httpd.daemon_threads = True
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(
            executable_path=BIN,
            args=["--no-sandbox"],
            env={**os.environ, "LD_LIBRARY_PATH": "/workspace/tmp/libs/root/usr/lib/x86_64-linux-gnu"},
        )
        pg = await b.new_page(viewport={"width": 1240, "height": 1754})
        await pg.goto(f"http://127.0.0.1:{PORT}/epk.html", wait_until="networkidle")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(1200)
        out = os.path.join(ROOT, "assets/downloads/Brandon-Choi-EPK-2026.pdf")
        await pg.pdf(path=out, format="A4", print_background=True,
                     margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        await b.close()
        print("bytes:", os.path.getsize(out))


httpd = serve()
try:
    asyncio.run(main())
finally:
    httpd.shutdown()
