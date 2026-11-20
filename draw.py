import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1024
HEIGHT = 1024

# Colors
BG_COLOR = "#F7F3EA"
NAVY_DARK = "#1E293B"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#D4C9B4"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#475569"
GOLD = "#E2B714"

CONTINENT_COLORS = {
    "Europe": "#C0392B",      # red
    "Asia": "#0E7C7B",        # teal (includes Middle East)
    "Africa": "#D98E00",      # ochre
    "North America": "#2E5FA3", # blue
    "South America": "#3E8E41", # green
    "Oceania": "#7A4FA3"      # purple
}

# Stories dataset
STORIES = [
    # Heroes 1-3
    {
        "num": 1, "continent": "Asia", "cat": "DIPLOMACY",
        "headline": "Trump, Xi and Putin hold first three-way summit",
        "deck": "The three leaders meet in Shenzhen, issuing a joint declaration on nuclear restraint, UN reform and ICC opposition. Trump and Putin met separately.",
        "lat": 22.5, "lon": 114.0, "badge": "1ST EVER · 3 LEADERS"
    },
    {
        "num": 2, "continent": "Europe", "cat": "COURTS",
        "headline": "World court: Myanmar committed genocide",
        "deck": "The ICJ finds Myanmar committed genocide against Rohingya in 2017 — the first time a state has been held responsible. Over 730,000 fled to Bangladesh.",
        "lat": 52.08, "lon": 4.31, "badge": "1ST STATE RULING · 9-6"
    },
    {
        "num": 3, "continent": "North America", "cat": "MARKETS",
        "headline": "Anthropic IPO: $81bn raised, $1.5tn value",
        "deck": "Claude-maker Anthropic raises a record $81.3 billion in its IPO, priced at $83 and opening at $111.50 — up 34% — valuing the company at about $1.5 trillion.",
        "lat": 40.7, "lon": -74.0, "badge": "$81BN · $1.5TN VALUE"
    },
    # Grid 4-15
    {
        "num": 4, "continent": "Asia", "cat": "CLIMATE",
        "headline": "COP31 ministers race to unblock talks",
        "deck": "Ministers meet in Antalya, Turkey, to break deadlock and adopt a final climate text.",
        "lat": 36.9, "lon": 30.7
    },
    {
        "num": 5, "continent": "Asia", "cat": "POLITICS",
        "headline": "Bangladesh violence: Yunus home torched",
        "deck": "Hasina supporters protest death sentence; Muhammad Yunus's ancestral home set on fire.",
        "lat": 23.8, "lon": 90.4
    },
    {
        "num": 6, "continent": "Asia", "cat": "ENERGY",
        "headline": "Hormuz crisis 'greatest threat ever' to energy",
        "deck": "IEA warns Middle East crisis threatens security; Brent crude falls to $89.59.",
        "lat": 26.5, "lon": 56.0
    },
    {
        "num": 7, "continent": "Asia", "cat": "WAR",
        "headline": "Gaza: Israel crosses ceasefire line",
        "deck": "Israel launches ground operation beyond 'yellow line' for tunnel; Hamas calls it violation.",
        "lat": 31.5, "lon": 34.45
    },
    {
        "num": 8, "continent": "North America", "cat": "POLITICS",
        "headline": "Senate rejects Iran war-powers curb, 51-48",
        "deck": "US Senate votes down resolution to end Iran war; Trump says he will 'see what happens'.",
        "lat": 38.9, "lon": -77.0
    },
    {
        "num": 9, "continent": "Europe", "cat": "WAR",
        "headline": "EU proposes 45bn euro loan for Ukraine",
        "deck": "EU proposes 2027 loan; UK pledges 1,000+ drones in 260m pound package.",
        "lat": 52.5, "lon": 13.4
    },
    {
        "num": 10, "continent": "Europe", "cat": "WAR",
        "headline": "Crimea bridge hit again, traffic halted",
        "deck": "Ukraine strikes Crimea bridge; Russia disputes damage scale as doctored videos circulate.",
        "lat": 45.3, "lon": 36.5
    },
    {
        "num": 11, "continent": "North America", "cat": "CULTURE",
        "headline": "Van Gogh sells for $190.4m, artist record",
        "deck": "1890 canvas sells at Sotheby's New York — most ever paid for a Van Gogh.",
        "lat": 40.7, "lon": -74.0
    },
    {
        "num": 12, "continent": "Oceania", "cat": "CLIMATE",
        "headline": "Fiji declares drought disaster",
        "deck": "Fiji declares national state of disaster as El Nino drought causes severe water shortages.",
        "lat": -18.14, "lon": 178.44
    },
    {
        "num": 13, "continent": "North America", "cat": "CRIME",
        "headline": "Haiti: 34 alleged gang members killed",
        "deck": "Police operation in Haiti leaves at least 34 alleged gang members dead.",
        "lat": 18.54, "lon": -72.34
    },
    {
        "num": 14, "continent": "Africa", "cat": "MIGRATION",
        "headline": "Migrant boat capsizes off Senegal",
        "deck": "Dozens missing after migrant boat bound for Europe capsizes off the coast of Senegal.",
        "lat": 14.7, "lon": -17.4
    },
    {
        "num": 15, "continent": "Africa", "cat": "WAR",
        "headline": "Ethiopia and Eritrea mass troops",
        "deck": "Forces gather along shared border, raising fears of wider war in the Horn of Africa.",
        "lat": 15.0, "lon": 39.0
    },
    # Also 16-35
    { "num": 16, "continent": "Asia", "cat": "WAR", "headline": "Kuwait repels first Iranian attack", "lat": 29.4, "lon": 47.98 },
    { "num": 17, "continent": "South America", "cat": "DIPLOMACY", "headline": "US and Venezuela sign military cooperation deal", "lat": 10.48, "lon": -66.88 },
    { "num": 18, "continent": "Europe", "cat": "POLITICS", "headline": "Denmark approves Greenland defence deal, 109-0", "lat": 55.68, "lon": 12.57 },
    { "num": 19, "continent": "Europe", "cat": "TECH", "headline": "UK tribunal upholds Apple data order", "lat": 51.5, "lon": -0.12 },
    { "num": 20, "continent": "Europe", "cat": "ECONOMY", "headline": "UK energy bills to rise 443 pounds a year", "lat": 53.48, "lon": -2.24 },
    { "num": 21, "continent": "Asia", "cat": "ECONOMY", "headline": "South Korea exports pass $1 trillion first time", "lat": 37.57, "lon": 126.98 },
    { "num": 22, "continent": "North America", "cat": "ECONOMY", "headline": "IMF: world public debt near 100% of GDP", "lat": 38.9, "lon": -77.0 },
    { "num": 23, "continent": "Asia", "cat": "DISASTER", "headline": "Indonesia refinery blast kills one in Cepu", "lat": -7.15, "lon": 111.6 },
    { "num": 24, "continent": "Asia", "cat": "POLITICS", "headline": "Indonesia passes asset law after 18 years", "lat": -6.2, "lon": 106.85 },
    { "num": 25, "continent": "Asia", "cat": "CLIMATE", "headline": "Indonesia fires burn 3m hectares, record smog", "lat": -2.0, "lon": 113.0 },
    { "num": 26, "continent": "Asia", "cat": "POLITICS", "headline": "Mongolia's president resigns; parliament accepts", "lat": 47.92, "lon": 106.92 },
    { "num": 27, "continent": "Asia", "cat": "POLITICS", "headline": "South Korea court overturns ex-PM Han's sentence", "lat": 35.18, "lon": 129.08 },
    { "num": 28, "continent": "Europe", "cat": "POLITICS", "headline": "Serbia elects student speaker, ending 14-yr hold", "lat": 44.79, "lon": 20.45 },
    { "num": 29, "continent": "Asia", "cat": "DIPLOMACY", "headline": "Japan and India deepen military cooperation", "lat": 35.68, "lon": 139.69 },
    { "num": 30, "continent": "Asia", "cat": "SECURITY", "headline": "North Korea expands uranium site, UN agency says", "lat": 39.8, "lon": 125.75 },
    { "num": 31, "continent": "Asia", "cat": "SECURITY", "headline": "Taiwan reports second Russian bomber overflight", "lat": 25.03, "lon": 121.57 },
    { "num": 32, "continent": "Oceania", "cat": "POLITICS", "headline": "Australia and China row over Darwin port lease", "lat": -12.46, "lon": 130.84 },
    { "num": 33, "continent": "Oceania", "cat": "COURTS", "headline": "NZ court: pay equity violated women's rights", "lat": -41.29, "lon": 174.78 },
    { "num": 34, "continent": "Asia", "cat": "SCIENCE", "headline": "Homo erectus teeth in China challenge theory", "lat": 22.4, "lon": 107.35 },
    { "num": 35, "continent": "North America", "cat": "MARKETS", "headline": "Nasdaq +0.42%, Nikkei +0.71%, Bitcoin $63,552", "lat": 40.7, "lon": -74.0 }
]

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def draw_grid_pictogram(draw, idx, gx, gy, cell_w, cell_h):
    x0 = gx + cell_w - 26
    y0 = gy + cell_h - 24
    x1 = gx + cell_w - 12
    y1 = gy + cell_h - 10
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2

    if idx == 0: # 4: Leaf
        draw.polygon([(cx, y0), (x1, cy), (cx, y1), (x0, cy)], fill="#3E8E41")
    elif idx == 1: # 5: Flame
        draw.polygon([(cx, y0), (x1, y1), (x0, y1)], fill="#C0392B")
    elif idx == 2: # 6: Oil drop
        draw.ellipse([x0 + 2, y0 + 2, x1 - 2, y1 - 2], fill="#D98E00")
    elif idx == 3: # 7: Shield
        draw.polygon([(x0, y0), (x1, y0), (x1, cy + 2), (cx, y1), (x0, cy + 2)], fill="#C0392B")
    elif idx == 4: # 8: Courthouse
        draw.rectangle([x0 + 2, cy, x1 - 2, y1], fill="#2E5FA3")
        draw.rectangle([x0 + 4, y0, x1 - 4, cy], fill="#2E5FA3")
    elif idx == 5: # 9: Cross/drone
        draw.line([x0, cy, x1, cy], fill="#2E5FA3", width=2)
        draw.line([cx, y0, cx, y1], fill="#2E5FA3", width=2)
    elif idx == 6: # 10: Bridge
        draw.line([x0, cy + 4, x1, cy + 4], fill="#1E293B", width=2)
        draw.line([x0 + 2, y0 + 4, x0 + 2, y1], fill="#1E293B", width=2)
        draw.line([x1 - 2, y0 + 4, x1 - 2, y1], fill="#1E293B", width=2)
    elif idx == 7: # 11: Frame
        draw.rectangle([x0, y0, x1, y1], outline="#E2B714", width=2)
    elif idx == 8: # 12: Sun
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill="#D98E00")
        draw.line([x0, cy, x1, cy], fill="#D98E00", width=1)
        draw.line([cx, y0, cx, y1], fill="#D98E00", width=1)
    elif idx == 9: # 13: Shield
        draw.polygon([(x0, y0), (x1, y0), (x1, y1), (cx, y1), (x0, y1)], fill="#2E5FA3")
    elif idx == 10: # 14: Boat
        draw.polygon([(x0, cy + 2), (x1, cy + 2), (x1 - 2, y1), (x0 + 2, y1)], fill="#D98E00")
        draw.line([cx, y0, cx, cy + 2], fill="#D98E00", width=1)
    elif idx == 11: # 15: Flag
        draw.line([x0 + 2, y0, x0 + 2, y1], fill="#C0392B", width=2)
        draw.polygon([(x0 + 2, y0), (x1, y0 + 4), (x0 + 2, y0 + 8)], fill="#C0392B")

def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    font_path_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    f_masthead_kicker = ImageFont.truetype(font_path_bold, 10)
    f_masthead_title = ImageFont.truetype(font_path_bold, 24)
    f_masthead_right = ImageFont.truetype(font_path_bold, 11)
    f_badge = ImageFont.truetype(font_path_bold, 9)
    f_num = ImageFont.truetype(font_path_bold, 12)
    f_hero_head = ImageFont.truetype(font_path_bold, 16)
    f_hero_deck = ImageFont.truetype(font_path_regular, 11)
    f_grid_head = ImageFont.truetype(font_path_bold, 13)
    f_grid_deck = ImageFont.truetype(font_path_regular, 9.5)
    f_section_title = ImageFont.truetype(font_path_bold, 12)
    f_also = ImageFont.truetype(font_path_regular, 9)
    f_also_bold = ImageFont.truetype(font_path_bold, 9)
    f_footer = ImageFont.truetype(font_path_regular, 10)

    # --- 1. MASTHEAD ---
    draw.rectangle([0, 0, WIDTH, 92], fill=NAVY_DARK)
    draw.text((20, 14), "THE DAY IN WORLD NEWS", fill=GOLD, font=f_masthead_kicker)
    draw.text((20, 28), "THURSDAY 19 NOVEMBER 2026", fill="#FFFFFF", font=f_masthead_title)

    draw.text((WIDTH - 20, 16), "35 STORIES · 6 CONTINENTS", fill="#FFFFFF", font=f_masthead_right, anchor="ra")

    # Legend row in masthead
    legend_x = WIDTH - 20
    legend_y = 52
    continents_list = [
        ("Europe", CONTINENT_COLORS["Europe"]),
        ("Asia", CONTINENT_COLORS["Asia"]),
        ("Africa", CONTINENT_COLORS["Africa"]),
        ("N. America", CONTINENT_COLORS["North America"]),
        ("S. America", CONTINENT_COLORS["South America"]),
        ("Oceania", CONTINENT_COLORS["Oceania"])
    ]
    current_x = WIDTH - 20
    for name, col in reversed(continents_list):
        bbox = draw.textbbox((0, 0), name, font=f_badge)
        text_w = bbox[2] - bbox[0]
        current_x -= (text_w + 16)
        draw.ellipse([current_x, legend_y + 4, current_x + 8, legend_y + 12], fill=col)
        draw.text((current_x + 12, legend_y + 1), name, fill="#CBD5E1", font=f_badge)
        current_x -= 10

    # --- 2. HERO ROW (Stories 1-3) ---
    hero_y = 104
    hero_h = 236
    hero_w = 328
    hero_gap = 18
    hero_x_start = 16

    for i in range(3):
        s = STORIES[i]
        hx = hero_x_start + i * (hero_w + hero_gap)
        hy = hero_y

        # Card bg & border
        draw.rectangle([hx, hy, hx + hero_w, hy + hero_h], fill=CARD_BG, outline=CARD_BORDER, width=1)

        # Illustration header area
        ill_h = 70
        draw.rectangle([hx, hy, hx + hero_w, hy + ill_h], fill="#F1F5F9")
        
        # Draw flat pictograms in illustration area
        if i == 0: # Shenzhen summit - three leaders (robed figures)
            for fx_offset in [65, 164, 263]:
                fx = hx + fx_offset
                draw.ellipse([fx - 6, hy + 18, fx + 6, hy + 30], fill="#0E7C7B")
                draw.polygon([(fx - 10, hy + 32), (fx + 10, hy + 32), (fx + 14, hy + 56), (fx - 14, hy + 56)], fill="#2E5FA3")
            draw.line([hx + 40, hy + 60, hx + 288, hy + 60], fill=NAVY_DARK, width=2)
        elif i == 1: # World court - gavel with scales
            sx = hx + 90
            draw.line([sx, hy + 15, sx, hy + 55], fill=NAVY_DARK, width=2)
            draw.line([sx - 20, hy + 22, sx + 20, hy + 22], fill=NAVY_DARK, width=2)
            draw.line([sx - 20, hy + 22, sx - 25, hy + 38], fill=TEXT_MUTED, width=1)
            draw.line([sx - 20, hy + 22, sx - 15, hy + 38], fill=TEXT_MUTED, width=1)
            draw.arc([sx - 28, hy + 36, sx - 12, hy + 46], 0, 180, fill="#C0392B")
            draw.line([sx + 20, hy + 22, sx + 15, hy + 38], fill=TEXT_MUTED, width=1)
            draw.line([sx + 20, hy + 22, sx + 25, hy + 38], fill=TEXT_MUTED, width=1)
            draw.arc([sx + 12, hy + 36, sx + 28, hy + 46], 0, 180, fill="#C0392B")
            gx_center = hx + 220
            draw.line([gx_center - 25, hy + 45, gx_center + 20, hy + 25], fill="#8B4513", width=4)
            draw.rectangle([gx_center + 15, hy + 18, gx_center + 35, hy + 38], fill="#A0522D", outline=NAVY_DARK, width=1)
        elif i == 2: # Anthropic IPO chart
            draw.line([hx + 30, hy + 55, hx + 290, hy + 55], fill="#CBD5E1", width=1)
            draw.line([hx + 30, hy + 50, hx + 90, hy + 45], fill="#2E5FA3", width=3)
            draw.line([hx + 90, hy + 45, hx + 150, hy + 35], fill="#2E5FA3", width=3)
            draw.line([hx + 150, hy + 35, hx + 230, hy + 20], fill="#2E5FA3", width=3)
            draw.line([hx + 230, hy + 20, hx + 290, hy + 12], fill="#2E5FA3", width=3)

        # Data badge pill inside illustration
        if "badge" in s:
            bw = draw.textbbox((0, 0), s["badge"], font=f_badge)[2] + 12
            draw.rounded_rectangle([hx + hero_w - bw - 10, hy + 8, hx + hero_w - 10, hy + 26], radius=4, fill="#E0F2FE", outline="#0284C7", width=1)
            draw.text((hx + hero_w - bw - 4, hy + 11), s["badge"], fill="#0369A1", font=f_badge)

        # Continent color tag
        c_col = CONTINENT_COLORS[s["continent"]]
        draw.rounded_rectangle([hx + 12, hy + ill_h + 10, hx + 12 + len(s["continent"])*6 + 16, hy + ill_h + 26], radius=3, fill=c_col)
        draw.text((hx + 20, hy + ill_h + 12), s["continent"].upper(), fill="#FFFFFF", font=f_badge)

        # Number badge
        num_circle_r = 11
        cx = hx + hero_w - 20
        cy = hy + ill_h + 18
        draw.ellipse([cx - num_circle_r, cy - num_circle_r, cx + num_circle_r, cy + num_circle_r], fill=c_col)
        draw.text((cx, cy), str(s["num"]), fill="#FFFFFF", font=f_num, anchor="mm")

        # Category tag
        draw.text((hx + 12, hy + ill_h + 34), s["cat"], fill=NAVY_DARK, font=f_badge)

        # Headline
        head_lines = wrap_text(s["headline"], f_hero_head, hero_w - 24, draw)
        text_y = hy + ill_h + 50
        for line in head_lines[:2]:
            draw.text((hx + 12, text_y), line, fill=TEXT_DARK, font=f_hero_head)
            text_y += 20

        # Deck
        deck_lines = wrap_text(s["deck"], f_hero_deck, hero_w - 24, draw)
        text_y += 4
        for line in deck_lines[:3]:
            draw.text((hx + 12, text_y), line, fill=TEXT_MUTED, font=f_hero_deck)
            text_y += 15

    # --- 3. GRID ROW 4-15 (4x3 grid) ---
    grid_x_start = 16
    grid_y_start = 352
    cell_w = 244
    cell_h = 122
    gap_x = 12
    gap_y = 10

    for idx in range(12):
        s = STORIES[3 + idx]
        row = idx // 4
        col = idx % 4
        gx = grid_x_start + col * (cell_w + gap_x)
        gy = grid_y_start + row * (cell_h + gap_y)

        # Cell background & border
        draw.rectangle([gx, gy, gx + cell_w, gy + cell_h], fill=CARD_BG, outline=CARD_BORDER, width=1)

        # Continent color & number badge
        c_col = CONTINENT_COLORS[s["continent"]]
        
        # Number badge
        num_r = 9
        nx = gx + cell_w - 14
        ny = gy + 14
        draw.ellipse([nx - num_r, ny - num_r, nx + num_r, ny + num_r], fill=c_col)
        draw.text((nx, ny), str(s["num"]), fill="#FFFFFF", font=f_badge, anchor="mm")

        # Category tag pill
        cat_w = draw.textbbox((0, 0), s["cat"], font=f_badge)[2] + 10
        draw.rounded_rectangle([gx + 10, gy + 10, gx + 10 + cat_w, gy + 24], radius=3, fill=c_col)
        draw.text((gx + 15, gy + 11), s["cat"], fill="#FFFFFF", font=f_badge)

        # Headline
        head_lines = wrap_text(s["headline"], f_grid_head, cell_w - 20, draw)
        ty = gy + 32
        for line in head_lines[:2]:
            draw.text((gx + 10, ty), line, fill=TEXT_DARK, font=f_grid_head)
            ty = ty + 16

        # Deck
        if "deck" in s:
            deck_lines = wrap_text(s["deck"], f_grid_deck, cell_w - 20, draw)
            ty += 2
            for line in deck_lines[:2]:
                draw.text((gx + 10, ty), line, fill=TEXT_MUTED, font=f_grid_deck)
                ty += 13

        # Add grid pictogram
        draw_grid_pictogram(draw, idx, gx, gy, cell_w, cell_h)

    # --- 4. BOTTOM SECTION: MAP & ALSO LIST ---
    bot_y = 746
    bot_h = 228

    # Bottom Left: WHERE IT HAPPENED (Map)
    map_box_w = 480
    map_x = 16
    draw.rectangle([map_x, bot_y, map_x + map_box_w, bot_y + bot_h], fill=CARD_BG, outline=CARD_BORDER, width=1)
    
    # Map header
    draw.rectangle([map_x, bot_y, map_x + map_box_w, bot_y + 24], fill=NAVY_DARK)
    draw.text((map_x + 10, bot_y + 6), "WHERE IT HAPPENED · 15 PINS & 20 REGIONAL DOTS", fill="#FFFFFF", font=f_section_title)

    # Render dot-matrix world map
    with open("worldmap.txt", "r") as f:
        map_lines = [line.rstrip("\n") for line in f if line.strip()]

    m_draw_x0 = map_x + 12
    m_draw_y0 = bot_y + 34
    m_draw_w = map_box_w - 24
    m_draw_h = bot_h - 44

    num_rows = len(map_lines)
    num_cols = len(map_lines[0]) if num_rows > 0 else 96

    cell_mw = m_draw_w / num_cols
    cell_mh = m_draw_h / num_rows

    for r_idx, r_line in enumerate(map_lines):
        for c_idx, ch in enumerate(r_line):
            if ch == '#':
                px = m_draw_x0 + c_idx * cell_mw
                py = m_draw_y0 + r_idx * cell_mh
                draw.rectangle([px, py, px + max(1, cell_mw - 0.2), py + max(1, cell_mh - 0.2)], fill="#475569")

    def project_latlon(lat, lon):
        px = m_draw_x0 + (lon + 180.0) / 360.0 * m_draw_w
        py = m_draw_y0 + (90.0 - lat) / 180.0 * m_draw_h
        return px, py

    for s in STORIES[15:]:
        px, py = project_latlon(s["lat"], s["lon"])
        col = CONTINENT_COLORS[s["continent"]]
        draw.ellipse([int(px - 3), int(py - 3), int(px + 3), int(py + 3)], fill=col)

    for s in STORIES[:15]:
        px, py = project_latlon(s["lat"], s["lon"])
        col = CONTINENT_COLORS[s["continent"]]
        r = 6
        draw.ellipse([int(px - r), int(py - r), int(px + r), int(py + r)], fill=col, outline="#FFFFFF", width=1)
        draw.text((px, py), str(s["num"]), fill="#FFFFFF", font=f_badge, anchor="mm")

    # Bottom Right: ALSO ON THURSDAY 19 NOVEMBER (Stories 16-35)
    also_x = 508
    also_w = 500
    draw.rectangle([also_x, bot_y, also_x + also_w, bot_y + bot_h], fill=CARD_BG, outline=CARD_BORDER, width=1)

    draw.rectangle([also_x, bot_y, also_x + also_w, bot_y + 24], fill=NAVY_DARK)
    draw.text((also_x + 10, bot_y + 6), "ALSO ON THURSDAY 19 NOVEMBER (STORIES 16-35)", fill="#FFFFFF", font=f_section_title)

    col1_items = STORIES[15:25]
    col2_items = STORIES[25:35]

    def draw_also_list(items, start_x, start_y):
        y_curr = start_y
        for s in items:
            text_str = f"{s['num']}  {s['headline']}"
            if len(text_str) > 52:
                text_str = text_str[:50] + "..."

            col = CONTINENT_COLORS[s["continent"]]
            draw.ellipse([start_x, y_curr + 3, start_x + 6, y_curr + 9], fill=col)
            draw.text((start_x + 12, y_curr), text_str, fill=TEXT_DARK, font=f_also)
            y_curr += 10.5

    draw_also_list(col1_items, also_x + 10, bot_y + 32)
    draw_also_list(col2_items, also_x + 256, bot_y + 32)

    # --- 5. FOOTER ---
    draw.rectangle([0, 984, WIDTH, HEIGHT], fill=NAVY_DARK)
    footer_text = "Every story happened or was first reported on Thursday 19 November 2026. Disputed claims are attributed. Sources: AP · Reuters · AFP · BBC · Al Jazeera · UN · Original drawings"
    draw.text((WIDTH / 2, 1004), footer_text, fill="#E2E8F0", font=f_footer, anchor="mm")

    output_path = "entry.png"
    img.save(output_path, "PNG")
    print(f"Successfully generated {output_path}. Size: {os.path.getsize(output_path)} bytes.")

if __name__ == "__main__":
    main()
