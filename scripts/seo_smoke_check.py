#!/usr/bin/env python3
"""Read-only, low-volume SEO smoke check.

Usage:
  python seo_smoke_check.py https://example.com
  python seo_smoke_check.py --timeout 20 --check-robots https://example.com
"""

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

DEFAULT_UA = "SEO-Skill-SmokeCheck/3.0"


def normalize_space(value):
    return " ".join(str(value or "").split())


def split_header_values(value):
    if not value:
        return []
    return [piece.strip() for piece in str(value).split(",") if piece.strip()]


class SEOHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = False
        self.title_parts = []
        self.meta = []
        self.links = []
        self.anchors = []
        self.h1 = 0
        self.h2 = 0
        self.json_ld = 0
        self.img_without_alt = 0
        self.og = {}

    def handle_starttag(self, tag, attrs):
        attrs_dict = {str(k).lower(): (v or "") for k, v in attrs}

        if tag == "title":
            self.title = True
        if tag == "meta":
            self.meta.append(attrs_dict)
            key = (attrs_dict.get("name") or attrs_dict.get("property") or "").strip().lower()
            if key.startswith("og:") and attrs_dict.get("content"):
                self.og[key] = attrs_dict.get("content").strip()
        if tag == "link":
            self.links.append(attrs_dict)
        if tag == "a":
            self.anchors.append(attrs_dict)
        if tag == "h1":
            self.h1 += 1
        if tag == "h2":
            self.h2 += 1
        if tag == "img" and not attrs_dict.get("alt", "").strip():
            self.img_without_alt += 1
        if tag == "script":
            script_type = (attrs_dict.get("type") or "").strip().lower()
            if script_type == "application/ld+json":
                self.json_ld += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.title = False

    def handle_data(self, data):
        if self.title:
            self.title_parts.append(data)


def meta_values(meta_entries, names):
    names_lower = {name.lower() for name in names}
    values = []
    for tag in meta_entries:
        key = (tag.get("name") or tag.get("property") or "").strip().lower()
        if key in names_lower and tag.get("content"):
            values.append(tag.get("content").strip())
    return values


def rel_is_canonical(link_tag):
    rel_value = (link_tag.get("rel") or "").strip().lower()
    rels = {item.lower() for item in re.split(r"\s+", rel_value) if item.strip()}
    return "canonical" in rels


def canonical_url_from_link(link_tags):
    for tag in link_tags:
        if rel_is_canonical(tag):
            href = (tag.get("href") or "").strip()
            if href:
                return href
    return ""


def http_redirect_chain(headers):
    if headers is None:
        return []
    values = []
    for key in ("Location", "location"):
        value = headers.get(key)
        if value:
            values.append(value)
    return values


def robots_noindex_values(robots_list, x_robots_list):
    tokens = []
    for item in robots_list:
        tokens.extend(split_header_values(item))
    for item in x_robots_list:
        tokens.extend(split_header_values(item))
    idx = []
    for token in tokens:
        value = token.lower()
        if "noindex" in value or "none" in value:
            idx.append(token)
    return idx


def count_internal_links(base_url, anchors):
    base_host = urllib.parse.urlparse(base_url).hostname or ""
    internal = 0
    external = 0
    for anchor in anchors:
        href = normalize_space(anchor.get("href") or "")
        if not href or href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        absolute = urllib.parse.urljoin(base_url, href)
        host = urllib.parse.urlparse(absolute).hostname or ""
        if host and host.lower() == base_host.lower():
            internal += 1
        elif host:
            external += 1
    return internal, external


def fetch_and_parse(url, timeout, max_bytes):
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            final_url = response.geturl()
            status = response.status
            headers = response.headers
            body = response.read(max_bytes).decode("utf-8", "replace")
            return {
                "requested_url": url,
                "final_url": final_url,
                "status": status,
                "headers": headers,
                "content": body,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(max_bytes).decode("utf-8", "replace")
        return {
            "requested_url": url,
            "final_url": exc.geturl(),
            "status": exc.code,
            "headers": exc.headers,
            "content": body,
        }
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc


def fetch_robots_txt(base_url, timeout):
    robots_url = urllib.parse.urljoin(base_url, "/robots.txt")
    try:
        req = urllib.request.Request(robots_url, headers={"User-Agent": DEFAULT_UA})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            text = response.read(200000).decode("utf-8", "replace")
            return {
                "url": robots_url,
                "status": response.status,
                "content": text,
            }
    except Exception:
        return {"url": robots_url, "status": None, "content": ""}


def run_checks(url, timeout, max_bytes, check_robots):
    result = fetch_and_parse(url, timeout, max_bytes)
    parser = SEOHTMLParser()
    parser.feed(result["content"])

    title = normalize_space(" ".join(parser.title_parts))
    meta_desc = meta_values(parser.meta, ["description"])
    meta_robots = meta_values(parser.meta, ["robots"])
    og_title = meta_values(parser.meta, ["og:title"])
    og_desc = meta_values(parser.meta, ["og:description"])
    canonical = canonical_url_from_link(parser.links)
    x_robots = split_header_values(result["headers"].get("X-Robots-Tag"))
    noindex_hits = robots_noindex_values(meta_robots, x_robots)

    internal_links, external_links = count_internal_links(result["final_url"], parser.anchors)

    report = {
        "requested_url": result["requested_url"],
        "final_url": result["final_url"],
        "status": result["status"],
        "content_type": result["headers"].get("Content-Type"),
        "title": title,
        "meta_description": meta_desc,
        "meta_robots": meta_robots,
        "x_robots_tag": x_robots,
        "canonical": canonical,
        "og_title": og_title,
        "og_description": og_desc,
        "h1_count": parser.h1,
        "h2_count": parser.h2,
        "json_ld_count": parser.json_ld,
        "images_without_alt": parser.img_without_alt,
        "total_links": len(parser.anchors),
        "internal_links": internal_links,
        "external_links": external_links,
        "has_noindex": bool(noindex_hits),
        "noindex_signals": noindex_hits,
        "note": "HTML response only; does not execute JavaScript or determine Google indexation.",
    }

    if check_robots:
        robots = fetch_robots_txt(result["final_url"], timeout)
        report["robots_txt"] = {
            "url": robots["url"],
            "status": robots["status"],
            "content": robots["content"][:2000],
        }

    return report


def main():
    parser = argparse.ArgumentParser(description="Read-only, low-volume SEO smoke check.")
    parser.add_argument("url", help="The URL to inspect.")
    parser.add_argument("--timeout", type=float, default=12.0, help="HTTP timeout in seconds (default: 12).")
    parser.add_argument("--max-bytes", type=int, default=2_000_000, help="Maximum HTML bytes to read (default: 2,000,000).")
    parser.add_argument("--check-robots", action="store_true", help="Fetch the /robots.txt file for the final URL.")
    args = parser.parse_args()

    url = args.url.strip()
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
        parser.error("Provide an http(s) URL")

    try:
        report = run_checks(url, args.timeout, args.max_bytes, args.check_robots)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"url": url, "error": str(exc)}, indent=2, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
