"""Paint the pygbag page around the square after a fresh web build."""
import re
from pathlib import Path

INDEX = Path("build/web/index.html")

# nginx sends Cross-Origin-Embedder-Policy: require-corp. A classic script
# from pygame-web is a no-cors request, and that CDN does not send
# Cross-Origin-Resource-Policy, so the browser drops it. The loader then
# waits forever on window.BrowserFS and the page stays on "Downloading...".
# crossorigin="anonymous" turns the request into CORS, which the CDN allows.
CORS_MARKER = "slide-quest-cdn-cors"
CORS_BOOTSTRAP = """<script data-slide-quest="cdn-cors">
/* slide-quest-cdn-cors */
(function () {
  var CDN = "pygame-web.github.io";
  function allow(el, value) {
    if (String(value).indexOf(CDN) === -1 || el.crossOrigin) return;
    el.crossOrigin = "anonymous";
  }
  var setAttr = HTMLScriptElement.prototype.setAttribute;
  HTMLScriptElement.prototype.setAttribute = function (name, value) {
    if (String(name).toLowerCase() === "src") allow(this, value);
    return setAttr.call(this, name, value);
  };
  var desc = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, "src");
  Object.defineProperty(HTMLScriptElement.prototype, "src", {
    configurable: true,
    enumerable: desc.enumerable,
    get: desc.get,
    set: function (value) {
      allow(this, value);
      desc.set.call(this, value);
    }
  });

  // The wheel CDN gzips the file but leaves Content-Length at the
  // compressed size. The loader allocates that many bytes, the last
  // chunk does not fit, and the zip is cut off. pygame.base is then
  // missing and the page stays on the navy background.
  var origFetch = window.fetch;
  window.fetch = function (input, init) {
    var url = typeof input === "string" ? input : (input && input.url) || "";
    var pending = origFetch.call(this, input, init);
    if (!/\.whl(\?|$)/.test(url)) return pending;
    return pending.then(function (response) {
      return response.arrayBuffer().then(function (buf) {
        var headers = new Headers(response.headers);
        headers.set("Content-Length", String(buf.byteLength));
        return new Response(buf, {
          status: response.status,
          statusText: response.statusText,
          headers: headers
        });
      });
    });
  };
})();
</script>"""


def allow_cdn_scripts(text):
    """Let pygame-web scripts load under Cross-Origin-Embedder-Policy."""
    if CORS_MARKER not in text:
        opener = "<html lang=\"en-us\">"
        if opener not in text:
            raise SystemExit("html opener missing from build/web/index.html")
        text = text.replace(opener, opener + CORS_BOOTSTRAP, 1)

    def tag(match):
        body = match.group(0)
        if "pygame-web.github.io" not in body or "crossorigin" in body.lower():
            return body
        if re.search(r"type\s*=\s*['\"]?module", body, re.I):
            return body
        return body[:-1] + " crossorigin=\"anonymous\">"

    return re.sub(r"<script\b[^>]*>", tag, text, flags=re.I)


def main():
    text = INDEX.read_text(encoding="utf-8")
    text = text.replace("#7f7f7f", "#0B2A51")
    text = text.replace("background-color:powderblue;", "background-color: #0B2A51;")
    anchor = "            margin: 0 auto;\n"
    frame = anchor + "            outline: 2px solid #43B8D6;\n            outline-offset: 0;\n"
    if anchor not in text:
        raise SystemExit("canvas CSS anchor missing from build/web/index.html")
    if "outline: 2px solid #43B8D6" not in text:
        text = text.replace(anchor, frame, 1)
    text = allow_cdn_scripts(text)
    INDEX.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
