#!/usr/bin/env python3
"""Read-only, low-volume SEO smoke check. Usage: python seo_smoke_check.py https://example.com"""
import argparse, json, re, urllib.parse, urllib.request
from html.parser import HTMLParser

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=False; self.titles=[]; self.meta=[]; self.links=[]; self.h1=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='title': self.title=True
        if tag=='h1': self.h1+=1
        if tag=='meta': self.meta.append(a)
        if tag=='link': self.links.append(a)
    def handle_endtag(self, tag):
        if tag=='title': self.title=False
    def handle_data(self, data):
        if self.title: self.titles.append(data)

def main():
    p=argparse.ArgumentParser(); p.add_argument('url'); args=p.parse_args()
    url=urllib.parse.urlparse(args.url)
    if url.scheme not in ('http','https') or not url.hostname: p.error('Provide an http(s) URL')
    req=urllib.request.Request(args.url, headers={'User-Agent':'SEO-Skill-SmokeCheck/2.0'})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            final=r.url; body=r.read(2_000_000).decode('utf-8','replace'); status=r.status; headers=r.headers
        t=Tags(); t.feed(body)
        report={'requested_url':args.url,'final_url':final,'status':status,'content_type':headers.get('Content-Type'),'x_robots_tag':headers.get('X-Robots-Tag'),'title':' '.join(t.titles).strip(),'h1_count':t.h1,'meta_description':[x.get('content') for x in t.meta if x.get('name','').lower()=='description'],'meta_robots':[x.get('content') for x in t.meta if x.get('name','').lower()=='robots'],'canonical':[x.get('href') for x in t.links if x.get('rel','').lower()=='canonical'],'hreflang':[{'lang':x.get('hreflang'),'href':x.get('href')} for x in t.links if x.get('hreflang')], 'note':'HTML response only; does not execute JavaScript or determine Google indexation.'}
        print(json.dumps(report,indent=2,ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'url':args.url,'error':str(e)})); raise SystemExit(1)
if __name__=='__main__': main()
