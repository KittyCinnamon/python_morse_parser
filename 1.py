from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

W, H = A4
PAGE_W = W - 5 * cm

# ── Palette ───────────────────────────────────────────────────────────────────
DARK        = colors.HexColor("#1a1a2e")
ACCENT      = colors.HexColor("#2563eb")
CODE_BG     = colors.HexColor("#1e293b")
CODE_FG     = colors.HexColor("#e2e8f0")
TABLE_HEAD  = colors.HexColor("#1e40af")
TABLE_ALT   = colors.HexColor("#f1f5f9")
RULE_COLOR  = colors.HexColor("#cbd5e1")
NOTE_BG     = colors.HexColor("#fef3c7")
NOTE_BORDER = colors.HexColor("#f59e0b")

# ── Base styles ───────────────────────────────────────────────────────────────
body_style = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5,
    textColor=DARK, leading=14, spaceAfter=6, alignment=TA_JUSTIFY)
bullet_style = ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.5,
    textColor=DARK, leading=14, spaceAfter=4, leftIndent=14)
h2_style = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=11,
    textColor=ACCENT, leading=15, spaceBefore=12, spaceAfter=4)
code_style = ParagraphStyle("Code", fontName="Courier", fontSize=8,
    textColor=CODE_FG, leading=12, backColor=CODE_BG)
note_style = ParagraphStyle("Note", fontName="Helvetica-Oblique", fontSize=9,
    textColor=colors.HexColor("#92400e"), leading=13, leftIndent=8,
    rightIndent=8, spaceBefore=8, spaceAfter=8, backColor=NOTE_BG,
    borderColor=NOTE_BORDER, borderWidth=1, borderPad=6)
closing_style = ParagraphStyle("Closing", fontName="Helvetica-Oblique",
    fontSize=9.5, textColor=colors.HexColor("#475569"), leading=14,
    alignment=TA_CENTER)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _th(text):
    return Paragraph(f"<b>{text}</b>", ParagraphStyle("th",
        fontName="Helvetica-Bold", fontSize=8.5,
        textColor=colors.white, alignment=TA_CENTER))

def h2(text):     return [Paragraph(text, h2_style)]
def body(text):   return [Paragraph(text, body_style)]
def bullet(text): return [Paragraph(f"• {text}", bullet_style)]
def spacer(n=8):  return [Spacer(1, n)]
def note(text):   return [Paragraph(f"⚠ {text}", note_style)]

def rule():
    return [Spacer(1, 4),
            HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR),
            Spacer(1, 6)]

def code_block(lines):
    t = Table(
        [[Preformatted("\n".join(lines), code_style, maxLineLength=90)]],
        colWidths=[PAGE_W]
    )
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), CODE_BG),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]

def data_table(header, rows, col_widths=None):
    if col_widths is None:
        col_widths = [PAGE_W / len(header)] * len(header)
    t = Table([header] + rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  TABLE_HEAD),
        ("TEXTCOLOR",      (0,0),(-1,0),  colors.white),
        ("FONTNAME",       (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0,0),(-1,-1), 8.5),
        ("LEADING",        (0,0),(-1,-1), 12),
        ("ALIGN",          (0,0),(-1,-1), "CENTER"),
        ("VALIGN",         (0,0),(-1,-1), "MIDDLE"),
        ("GRID",           (0,0),(-1,-1), 0.4, RULE_COLOR),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [colors.white, TABLE_ALT]),
        ("LEFTPADDING",    (0,0),(-1,-1), 8),
        ("RIGHTPADDING",   (0,0),(-1,-1), 8),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
    ]))
    return [Spacer(1, 6), t, Spacer(1, 8)]

def section_num(n, label):
    t = Table([[
        Paragraph(f"<font color='white' size='11'><b>{n}</b></font>",
            ParagraphStyle("b", fontName="Helvetica-Bold", fontSize=11,
                           textColor=colors.white, alignment=TA_CENTER)),
        Paragraph(f"<font color='white' size='11'><b>  {label}</b></font>",
            ParagraphStyle("b2", fontName="Helvetica-Bold", fontSize=11,
                           textColor=colors.white))
    ]], colWidths=[1.2 * cm, PAGE_W - 1.2 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), ACCENT),
        ("BACKGROUND",    (0,0),(0,0),   colors.HexColor("#1d4ed8")),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    return [Spacer(1, 14), t, Spacer(1, 8)]

def proof_box(items):
    """Light green box for mathematical proofs/derivations."""
    inner = []
    for item in items:
        inner.append(Paragraph(item, ParagraphStyle("pb",
            fontName="Helvetica", fontSize=9,
            textColor=DARK, leading=13, spaceAfter=3)))
    t = Table([[inner]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), colors.HexColor("#f0fdf4")),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("BOX",           (0,0),(-1,-1), 0.8, colors.HexColor("#16a34a")),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]

def case_box(label, items):
    """Comparison box (worst-case vs optimum)."""
    inner = [Paragraph(f"<b>{label}</b>", ParagraphStyle("cl",
        fontName="Helvetica-Bold", fontSize=9.5,
        textColor=colors.HexColor("#1e40af"), leading=13, spaceAfter=4))]
    for item in items:
        inner.append(Paragraph(f"• {item}", ParagraphStyle("ci",
            fontName="Helvetica", fontSize=9,
            textColor=DARK, leading=13, spaceAfter=2)))
    t = Table([[inner]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), colors.HexColor("#eff6ff")),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("BOX",           (0,0),(-1,-1), 0.8, ACCENT),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]

# ── Document ──────────────────────────────────────────────────────────────────
pdf_path = "lezione 12.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title="Makespan, Max-Cut e Bin Packing",
    author="Appunti")

story = []

# ── Cover ─────────────────────────────────────────────────────────────────────
title_style = ParagraphStyle("T", fontName="Helvetica-Bold", fontSize=17,
    textColor=DARK, leading=23, spaceAfter=4, alignment=TA_CENTER)
sub_style = ParagraphStyle("S", fontName="Helvetica", fontSize=11,
    textColor=colors.HexColor("#64748b"), leading=14, spaceAfter=18,
    alignment=TA_CENTER)

story.append(Spacer(1, 1*cm))
story.append(Paragraph("Analisi Strutturale degli Algoritmi d'Approssimazione", title_style))
story.append(Paragraph("Makespan · Max-Cut · Bin Packing", title_style))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="60%", thickness=2, color=ACCENT, hAlign="CENTER"))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Load Balancing · Partizionamento di Grafi · Ottimizzazione Combinatoria", sub_style))
story.append(Spacer(1, 0.6*cm))

story += body(
    "Nel dominio della complessità computazionale, la risoluzione di problemi <b>NP-hard</b> pone "
    "una sfida fondamentale: l'impossibilità di determinare una soluzione ottima in tempo polinomiale "
    "al crescere delle dimensioni dell'input. In tali scenari, gli <b>algoritmi d'approssimazione</b> "
    "rappresentano un compromesso strategico tra efficienza temporale e qualità della soluzione, "
    "fornendo garanzie matematiche sulla vicinanza del risultato ottenuto rispetto a quello ideale. "
    "Un algoritmo è detto ρ-approssimante se, per ogni istanza, la soluzione fornita non devia "
    "dall'ottimo per un fattore superiore a ρ."
)

# ── Sezione 1 ─────────────────────────────────────────────────────────────────
story += section_num("1", "Minimizzazione del Makespan (C_max)")

story += body(
    "La gestione delle risorse in ambienti di calcolo distribuito richiede un "
    "<b>bilanciamento del carico</b> raffinato. L'obiettivo è distribuire <i>n</i> lavori "
    "su <i>m</i> macchine identiche minimizzando il makespan "
    "C<sub>max</sub> = max<sub>i</sub>(carico macchina <i>i</i>)."
)

story += data_table(
    [_th("Istanza d'esempio"), _th("Distribuzione ottima"), _th("C*_max")],
    [["P = [11, 10, 8, 7, 6, 5], m = 3",
      "[[11,5], [10,6], [8,7]]",
      "16"]],
    col_widths=[6*cm, 5*cm, PAGE_W-11*cm]
)

story += h2("Algoritmo Greedy Online — Garanzia ρ < 2")
story += body(
    "L'approccio greedy assegna ogni lavoro alla macchina con il <b>carico minore</b> al momento "
    "dell'elaborazione. Non richiede la conoscenza dei lavori futuri (<i>online</i>)."
)
story += proof_box([
    "Dimostrazione: sia k l'ultimo lavoro a terminare e t_k il suo istante di inizio.",
    "Tutte le macchine hanno carico ≥ t_k  →  m · t_k < S  →  t_k < S/m.",
    "Poiché S/m ≤ C*_max e p_k ≤ C*_max, si ottiene:",
    "C_max = t_k + p_k  <  S/m + C*_max  ≤  2 · C*_max     ∎",
])

story += h2("Caso Limite del Greedy")
story += case_box("Worst-case — m(m−1) lavori di durata 1 + 1 lavoro di durata m", [
    "Greedy distribuisce i lavori piccoli uniformemente → carico m−1 per macchina.",
    "L'ultimo lavoro di durata m porta C_max = 2m − 1.",
    "Ottimo = m   →   rapporto → 2 asintoticamente.",
])

story += h2("Ottimizzazione LPT (Offline) — Garanzia ρ ≤ 4/3")
story += body(
    "L'algoritmo <b>LPT (Longest Processing Time)</b> ordina i lavori in modo decrescente "
    "prima dell'assegnazione. Il pre-ordinamento riduce il rapporto da 2 a 4/3."
)
story += bullet(
    "<b>Caso p_k ≤ 1/3 · C*_max:</b> il limite 4/3 deriva da C_max < C*_max + p_k ≤ 4/3 · C*_max."
)
story += bullet(
    "<b>Caso p_k > 1/3 · C*_max:</b> ogni macchina ospita al più 2 lavori; LPT produce la soluzione ottima."
)

story += h2("Implementazione Python — O(n log m)")
story += code_block([
    "import heapq",
    "",
    "def lpt_schedule(durata_lavori, num_macchine):",
    "    # Strategia Offline: ordinamento decrescente",
    "    lavori_ordinati = sorted(durata_lavori, reverse=True)",
    "",
    "    # Min-heap per ottenere la macchina più scarica in O(log m)",
    "    heap_macchine = [(0, i) for i in range(num_macchine)]",
    "    carichi = [0] * num_macchine",
    "",
    "    for durata in lavori_ordinati:",
    "        carico_min, idx = heapq.heappop(heap_macchine)",
    "        nuovo_carico = carico_min + durata",
    "        carichi[idx] = nuovo_carico",
    "        heapq.heappush(heap_macchine, (nuovo_carico, idx))",
    "",
    "    return max(carichi), carichi",
])
story += note(
    "L'uso del min-heap porta la complessità da O(nm) a O(n log m): "
    "determinante per istanze con molte macchine."
)

# ── Sezione 2 ─────────────────────────────────────────────────────────────────
story += section_num("2", "Il Problema del Massimo Taglio (MAX-CUT)")

story += body(
    "Dato un grafo G = (V, E), il problema MAX-CUT richiede di partizionare V in due insiemi "
    "A e B <b>massimizzando il numero di archi che attraversano il taglio</b> (un estremo in A, "
    "l'altro in B). L'algoritmo greedy assegna ogni nodo all'insieme che massimizza il taglio "
    "locale rispetto ai nodi già processati."
)

story += h2("Dimostrazione del Rapporto ρ ≤ 2")
story += body(
    "Si introduce la <b>responsabilità del vertice</b> r<sub>i</sub>: numero di vicini di <i>i</i> "
    "con indice minore già assegnati."
)
story += proof_box([
    "Limite superiore:  Σ r_i  =  m  (ogni arco contribuisce esattamente una volta)",
    "                   K*  ≤  m",
    "",
    "Limite inferiore:  ad ogni passo i, il greedy taglia almeno r_i / 2 archi.",
    "                   K  ≥  Σ(r_i / 2)  =  m / 2",
    "",
    "Combinando:        K*  ≤  m  ≤  2K     →     ρ  ≤  2     ∎",
])

story += h2("Caso Limite — Grafo a Due Hub")
story += case_box(
    "Grafo: v1 e v2 connessi a tutti gli altri n−2 nodi",
    [
        "Greedy: v1 ∈ A, v2 ∈ B. Ogni nodo successivo ha un vicino in A e uno in B → taglia 1 arco.",
        "Risultato greedy: K = 1 + (n−2) = n−1.",
        "Ottimo: v1, v2 ∈ A, tutti gli altri in B → ogni nodo in B contribuisce 2 archi.",
        "K* = 2(n−2)   →   rapporto K*/K → 2 per n → ∞.",
    ]
)

story += h2("Implementazione Python — O(n + m)")
story += code_block([
    "def EuristicaTaglioMassimo(G):",
    "    n = len(G)",
    "    IA, IB = [0] * n, [0] * n  # Incentivi verso A e B",
    "    A = []",
    "    for i in range(n):",
    "        if IA[i] >= IB[i]:",
    "            A.append(i)",
    "            for u in G[i]:",
    "                # Aggiorna solo nodi futuri (greedy online)",
    "                if u > i: IB[u] += 1",
    "        else:",
    "            for u in G[i]:",
    "                if u > i: IA[u] += 1",
    "    return A",
])

# ── Sezione 3 ─────────────────────────────────────────────────────────────────
story += section_num("3", "Il Problema del Bin Packing — Euristica Next Fit")

story += body(
    "Il <b>Bin Packing</b> mira a minimizzare il numero di contenitori di capacità <i>c</i> "
    "necessari per ospitare <i>n</i> oggetti. L'euristica <b>Next Fit</b> opera con memoria "
    "limitata: mantiene aperto un solo contenitore corrente. Se l'oggetto corrente non vi entra, "
    "il contenitore viene sigillato e se ne apre uno nuovo."
)

story += h2("Dimostrazione del Rapporto ρ < 2")
story += proof_box([
    "Proprietà chiave: la somma degli oggetti in due bin consecutivi B_i e B_{i+1} > c.",
    "(Se così non fosse, il primo oggetto di B_{i+1} sarebbe stato inserito in B_i.)",
    "",
    "Sia s la somma totale delle dimensioni e k il numero di bin usati:",
    "   Σ coppie (B_{2i-1} + B_{2i}) > c  →  (k−1)/2 · c < s",
    "",
    "Poiché l'ottimo soddisfa s ≤ c · k*:",
    "   (k−1)/2 < k*   →   k < 2k* + 1   →   k ≤ 2k*     ∎",
])

story += h2("Caso Limite — Sequenza Alternata c/2 e 1")
story += case_box(
    "Input: 2c oggetti con dimensioni alternate c/2 e 1",
    [
        "Next Fit: inserisce (c/2 + 1) per bin; il successivo c/2 non entra → k = c bin.",
        "Ottimo: c/2 oggetti da c/2 a coppie (c/2 bin) + tutti gli 1 in 1 bin → k* = c/2 + 1.",
        "Rapporto k / k* → 2 al crescere di c.",
    ]
)

story += h2("Implementazione Python — O(n)")
story += code_block([
    "def inscatolamento(L, c):",
    "    if not L: return []",
    "    n = len(L)",
    "    S = [[0]]",
    "    peso_residuo = c - L[0]",
    "    for i in range(1, n):",
    "        if peso_residuo >= L[i]:",
    "            S[-1].append(i)",
    "            peso_residuo -= L[i]",
    "        else:",
    "            S.append([i])",
    "            peso_residuo = c - L[i]",
    "    return S",
])

# ── Sezione 4 — Tabella comparativa ──────────────────────────────────────────
story += section_num("4", "Sintesi Comparativa")

story += data_table(
    [_th("Problema"), _th("Algoritmo"), _th("ρ"), _th("Complessità")],
    [
        ["Makespan (C_max)", "LPT — Longest Processing Time", "4/3", "O(n log m)"],
        ["MAX-CUT",          "Greedy (Local Improvement)",    "2",   "O(n + m)"],
        ["Bin Packing",      "Next Fit",                      "2",   "O(n)"],
    ],
    col_widths=[4*cm, 5.5*cm, 1.5*cm, PAGE_W-11*cm]
)

story += body(
    "L'analisi dimostra come la <b>scelta delle strutture dati</b> sia determinante: "
    "l'integrazione di un min-heap nel Makespan trasforma un'intuizione greedy in uno strumento "
    "ad alte prestazioni. Il passaggio da O(nm) a O(n log m) non è un dettaglio implementativo, "
    "ma una scelta architetturale con impatto diretto sulla scalabilità del sistema."
)

story += spacer(12)
story += rule()
story.append(Paragraph(
    "Sebbene gli algoritmi d'approssimazione non garantiscano l'ottimalità assoluta, "
    "la loro capacità di fornire <b>soluzioni entro limiti teorici certi</b> in tempi lineari "
    "o log-lineari li rende strumenti indispensabili nell'informatica applicata.",
    closing_style
))

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print("PDF generato:", pdf_path)