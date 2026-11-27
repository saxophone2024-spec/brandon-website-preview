#!/usr/bin/env python3
"""Parse Schedule_Brandon Choi Google Doc text into structured schedule records."""
import json, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

MONTHS_EN = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def has_hangul(s):
    return any('\uac00' <= ch <= '\ud7a3' for ch in s)

def has_latin_word(s):
    return re.search(r'[A-Za-z]{2,}', s) is not None

HDR_MONTH = re.compile(r'(\d{1,2})\s*월')
YEAR = re.compile(r'(20\d{2})')

def clean(s):
    s = s.replace('\u2002', ' ').replace('\u00a0', ' ').replace('\u000b', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s*[–—-]\s*$', '', s)
    s = s.strip(' |').strip()
    return s.strip()

# manual corrections where the doc has an English-only or mistyped line
KO_OVERRIDE = {
    (2026, 1, 5): "서울시의 밤 – 서울고등학교 개교 80주년 기념 갈라 콘서트",
}
VENUE_OVERRIDE = {
    (2026, 12, 27): "Pyeongtaek Art Center",   # doc's English line repeated the Yongin hall by mistake
}
EN_OVERRIDE = {
    (2026, 1, 5): "Seoul Citizens’ Night – Seoul High School 80th Anniversary Gala Concert",
    (2026, 10, 31): "Autumn Music Festival, Changdong",
    (2025, 12, 24): "Collaboration with the National Orchestra of Korea",
}

def parse(text):
    recs = []
    year = None
    month = None
    month_label = None
    for raw in text.split('\n'):
        line = raw.strip()
        if not line:
            continue
        if line.startswith('📅') or (line.startswith(('Brandon', '브랜든')) and 'Schedule' in line) or '일정표' in line:
            m = YEAR.search(line)
            if m: year = int(m.group(1))
            month = None
            continue
        if line.startswith('🗓️') or re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December)\b', line):
            m = HDR_MONTH.search(line)
            if m:
                month = int(m.group(1))
            else:
                for i, name in enumerate(MONTHS_EN, 1):
                    if name in line:
                        month = i; break
            month_label = clean(re.sub(r'^🗓️\s*', '', line))
            continue
        m = re.match(r'^(\d{1,2})\.(\d{1,2})(?:\s*[–—-]\s*(?:(\d{1,2})\.(\d{1,2})(?!\d)|(\d{1,2})(?!\d)))?\s*[–—-]?\s*(.*)$', line, re.S)
        if m:
            mo = int(m.group(1)); day = int(m.group(2))
            if m.group(3):                      # range written M.D – M.D
                end_month = int(m.group(3)); end_day = int(m.group(4))
            else:
                end_month = None; end_day = int(m.group(5)) if m.group(5) else None
            recs.append(build(year, mo, day, end_day, end_month, m.group(6), month_label))
        elif month:
            r = build(year, month, None, None, None, line, month_label)
            r['spanLabel'] = month_label
            recs.append(r)
    return recs

def build(year, mo, day, end_day, end_month, rest, month_label):
    raw_parts = []
    for seg in rest.split('\u000b'):
        for part in re.split(r'\s*\|\s*', seg):
            part = part.strip()
            if part:
                raw_parts.append(part)

    ko_parts, en_parts, venue, notes_ko = [], [], '', []
    for i, part in enumerate(raw_parts):
        # pull an inline venue ("@ Hall", "@루비체임버스홀")
        if '@' in part:
            head, tail = re.split(r'\s*@\s*', part, maxsplit=1)
            if tail:
                venue = clean(tail)
            part = head.strip()
            if not part:
                continue
        if re.match(r'(?i)^artistic director', part):
            en_parts.append(clean(part)); continue
        if part.startswith('(') and has_hangul(part):
            notes_ko.append(part.strip('()')); continue
        if i == 0:
            (ko_parts if has_hangul(part) else en_parts).append(clean(part))
        else:
            if has_hangul(part) and not has_latin_word(part):
                ko_parts.append(clean(part))
            else:
                en_parts.append(clean(part))

    ko = clean(' · '.join(ko_parts))
    en = clean(' · '.join(en_parts))
    key = (year, mo, day)
    if key in KO_OVERRIDE:
        ko = KO_OVERRIDE[key]
    if key in EN_OVERRIDE:
        en = EN_OVERRIDE[key]
    if key in VENUE_OVERRIDE:
        venue = VENUE_OVERRIDE[key]
    if notes_ko:
        ko = (ko + ' (' + ' '.join(notes_ko) + ')').strip()
    if not en: en = ko
    if not ko: ko = en
    return {
        'year': year, 'month': mo, 'day': day, 'endDay': end_day, 'endMonth': end_month,
        'ko': ko, 'en': en, 'venue': venue, 'monthLabel': month_label,
    }

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'doc.txt')
    text = open(src, encoding='utf-8').read()
    recs = parse(text)
    json.dump(recs, open(os.path.join(HERE, 'records.json'), 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print('total', len(recs), Counter(r['year'] for r in recs))
    print('empty ko', sum(1 for r in recs if not r['ko']))
    for r in recs:
        if r['year'] == 2026 and (r['month'], (r['day'] or 0)) >= (11, 20):
            print(r)
