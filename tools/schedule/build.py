#!/usr/bin/env python3
"""Build the #schedule section markup from records.json and inject into index.html."""
import json, re, html, os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

MONTHS_EN = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
TODAY = date(2026, 11, 28)

recs = json.load(open(os.path.join(HERE, 'records.json'), encoding='utf-8'))


def esc(s):
    return html.escape(s, quote=False)


def date_label(r):
    if not r.get('day'):
        # month-level item (e.g. Jan–Feb recording session)
        lab = r.get('spanLabel') or ''
        nums = re.findall(r'(\d{1,2})\s*월', lab)
        if len(nums) >= 2:
            return f"{int(nums[0])}–{int(nums[1])}"
        return f"{r['month']}"
    d = f"{r['month']}.{r['day']}"
    if r.get('endDay'):
        if r.get('endMonth') and r['endMonth'] != r['month']:
            d += f"–{r['endMonth']}.{r['endDay']}"
        else:
            d += f"–{r['endDay']}"
    return d


def iso(r):
    if not r.get('day'):
        return None
    return date(r['year'], r['month'], r['day']).isoformat()


def bilingual(ko, en, cls):
    if ko == en:
        return f'<span class="{cls}">{esc(ko)}</span>'
    return (f'<span class="{cls}"><span class="ko">{esc(ko)}</span>'
            f'<span class="en">{esc(en)}</span></span>')



# a Korean title that already names the hall makes the English venue line redundant
REDUNDANT_KO = {
    "Lotte Concert Hall": ["롯데콘서트홀"],
    "Yongin Poeun Art Hall": ["용인포은아트홀"],
    "Pyeongtaek Art Center": ["평택아트센터"],
    "Goyang Aram Nuri Arts Center": ["고양아람누리"],
    "Atmosphere Music Hall": ["앳모스피어"],
    "Mapo Art Center": ["마포아트센터"],
    "Cheonan Arts Center": ["천안예술"],
    "Busan": ["부산"],
    "Suwon": ["수원"],
    "Yeongsan Art Hall": ["영산아트홀"],
    "Starfield Library, COEX": ["별마당"],
    "Gwangju Museum of Art": ["광주시립미술관"],
    "White Wave Art Center": ["흰물결"],
    "Seoul Arts Center, IBK Chamber Hall": ["예술의전당"],
    "Playlist Wonju": ["플레이리스트"],
    "Jangcheon Art Hall": ["장천아트홀"],
    "Busan Yeongdo Cultural Arts Center": ["영도문화예술회관"],
    "Bijoux Art Project": ["비쥬"],
    "COEX": ["코엑스"],
    "Evans": ["에반스"],
    "Korea Classic Saxophone Association": ["KCSA"],
}


def show_venue(r):
    v = r.get('venue')
    if not v:
        return False
    for marker in REDUNDANT_KO.get(v, []):
        if marker in r['ko']:
            return False
    if v.lower() in r['en'].lower():
        return False
    return True


def row(r, indent='', with_flag=False):
    parts = []
    d = date_label(r)
    dt = iso(r)
    attr = f' data-date="{dt}"' if dt else ''
    flag = ''
    parts.append(f'<li class="sched-row"{attr}>')
    if not r.get('day'):
        parts.append(f'  <span class="sched-row__date"><span class="ko">{esc(d)}월</span><span class="en">Jan–Feb</span></span>')
    else:
        parts.append(f'  <span class="sched-row__date">{esc(d)}</span>')
    parts.append('  <span class="sched-row__body">')
    parts.append('    ' + bilingual(r['ko'], r['en'], 'sched-row__title'))
    if show_venue(r):
        parts.append(f'    <span class="sched-row__venue">{esc(r["venue"])}</span>')
    parts.append('  </span>')
    if with_flag:
        parts.append('  <span class="sched-row__flag">Next</span>')
    parts.append('</li>')
    out = '\n'.join(parts)
    if indent:
        out = '\n'.join(indent + ln for ln in out.split('\n'))
    return out


def group_by_month(rows):
    out = []
    for r in rows:
        if not out or out[-1][0] != r['month']:
            out.append((r['month'], []))
        out[-1][1].append(r)
    return out


def sort_key(r):
    return (r['year'], r['month'], r['day'] or 0)


# ---- upcoming: 2026 from today onward, then any later year ----
upcoming = [r for r in recs if (r['year'], r['month'], r['day'] or 0) >= (TODAY.year, TODAY.month, TODAY.day)]
upcoming.sort(key=sort_key)

lines = []
A = lines.append

A('<!-- SCHEDULE -->')
A('<section class="section" id="schedule">')
A('  <div class="shell">')
A('    <div class="head reveal">')
A('      <div>')
A('        <span class="label"><b>03</b> Schedule</span>')
A('        <h2 class="h2" style="margin-top:14px"><span class="ko">공연 일정</span><span class="en">Schedule</span></h2>')
A('      </div>')
A('      <p><span class="ko">다가오는 무대와 2022년부터의 전체 기록. 초청·섭외는 언제든 문의 주세요.</span>'
  '<span class="en">Upcoming dates and every performance since 2022. For invitations, get in touch any time.</span></p>')
A('    </div>')
A('')
A('    <div class="sched">')
A('      <div class="sched__head">')
A('        <h3 class="sched__h"><span class="ko">다가오는 공연</span><span class="en">Upcoming</span></h3>')
A(f'        <span class="sched__count" id="sched-count">{len(upcoming)} <span class="ko">공연</span><span class="en">dates</span></span>')
A('      </div>')
A('      <ul class="sched-list" id="sched-upcoming">')
for i, r in enumerate(upcoming):
    A(row(r, '        ', with_flag=(i == 0)))
A('      </ul>')
A('      <p class="sched__empty" id="sched-empty" hidden>')
A('        <span class="ko">현재 확정된 공연이 없습니다. 다음 시즌 일정은 확정되는 대로 이곳에 올립니다.</span>'
  '<span class="en">No dates are currently announced. The next season appears here as it is confirmed.</span>')
A('      </p>')
A('      <div class="note-bar">')
A('        <p><span class="ko">초청 공연·강연·마스터클래스는 일정 조율이 가능합니다. 프라이빗 콘서트 문의도 환영합니다.</span>'
  '<span class="en">Invited concerts, talks and masterclasses can be scheduled around your dates. Private concerts welcome.</span></p>')
A('        <a class="btn btn--sm btn--ghost" href="#contact"><span class="ko">섭외 문의</span><span class="en">Enquire</span><span class="arrow">→</span></a>')
A('      </div>')
A('    </div>')
A('')
A('    <div class="sched-archive">')
A('      <div class="sched__head">')
A('        <h3 class="sched__h"><span class="ko">전체 일정</span><span class="en">Full archive</span></h3>')
A('        <span class="sched__count">2022 — 2026</span>')
A('      </div>')
for year in sorted({r['year'] for r in recs}, reverse=True):
    yr = sorted([r for r in recs if r['year'] == year], key=sort_key)
    A(f'      <details class="sched-year" data-year="{year}">')
    A(f'        <summary><span class="sched-year__num">{year}</span>'
      f'<span class="sched-year__meta">{len(yr)}<span class="ko">회</span><span class="en"> dates</span></span>'
      f'<span class="sched-year__chev" aria-hidden="true"></span></summary>')
    A('        <div class="sched-year__body">')
    for m, rows in group_by_month(yr):
        A('          <div class="sched-month">')
        A(f'            <span class="sched-month__label">{m:02d} · {MONTHS_EN[m]}</span>')
        A('            <ul class="sched-list">')
        for r in rows:
            A(row(r, '              '))
        A('            </ul>')
        A('          </div>')
    A('        </div>')
    A('      </details>')
A('    </div>')
A('  </div>')
A('</section>')
section = '\n'.join(lines)

page = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
if '<!-- SCHEDULE -->' in page:
    start = page.index('<!-- SCHEDULE -->')
    end = page.index('<!-- EPK -->')
    page = page[:start] + section + '\n\n' + page[end:]
else:
    page = page.replace('\n<!-- EPK -->', '\n' + section + '\n\n<!-- EPK -->', 1)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
print('section chars', len(section), 'rows', len(recs), 'upcoming', len(upcoming))
