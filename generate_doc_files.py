#!/usr/bin/env python3
"""
generate_doc_files.py - Render clean, professional engineering diagrams and compile the complete 35-section Research Audit Report into DOCX and PDF formats.

Produces:
1. project-documentation/diagrams/system_architecture.png
2. project-documentation/diagrams/authentication_flow.png
3. project-documentation/PROJECT_RESEARCH_REPORT.docx (Full 35-Section Word Document)
4. project-documentation/PROJECT_RESEARCH_REPORT.pdf (Full 35-Section PDF Document)
"""

import os
import re
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DOCS_DIR = Path(__file__).parent / "project-documentation"
DIAGRAMS_DIR = DOCS_DIR / "diagrams"
MD_REPORT_PATH = DOCS_DIR / "PROJECT_RESEARCH_REPORT.md"

def render_system_architecture_image():
    """Render a clean engineering diagram with white background, black text, and standard shapes."""
    fig, ax = plt.subplots(figsize=(15.5, 8.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    stages = [
        ("STAGE 1: INPUT & WORKFLOW", 0.5, 4.3),
        ("STAGE 2: DETERMINISTIC ENGINE", 4.7, 8.7),
        ("STAGE 3: AUDIT ARTIFACTS", 9.1, 12.7),
        ("STAGE 4: DOCS & VALIDATION", 13.1, 17.6)
    ]

    for title, x_min, x_max in stages:
        rect = patches.FancyBboxPatch((x_min, 0.4), x_max - x_min, 7.6, boxstyle="square,pad=0.15",
                                      ec='#cbd5e1', fc='#f8fafc', lw=1.2, linestyle='--')
        ax.add_patch(rect)
        ax.text((x_min + x_max)/2, 7.65, title, color='#475569', fontsize=10, fontweight='bold', ha='center', va='center')

    nodes = {
        "user": ("User / AI Agent", "Input Trigger", "oval", 2.4, 5.8, 3.2, 1.2),
        "skill": ("SKILL.md Workflow", "26-Step Controller", "rect", 2.4, 2.4, 3.2, 1.2),

        "inv": ("inventory_repository.py", "22 File Categories", "rect", 6.7, 6.6, 3.4, 0.95),
        "tech": ("detect_technology_stack.py", "28 Tech Categories", "rect", 6.7, 5.2, 3.4, 0.95),
        "struct": ("analyze_structure.py", "Entry Points & Routes", "rect", 6.7, 3.8, 3.4, 0.95),
        "sec": ("detect_secrets_safely.py", "Safe Secret Auditor", "rect", 6.7, 2.4, 3.4, 0.95),
        "evid": ("collect_code_evidence.py", "Line Evidence Collector", "rect", 6.7, 1.0, 3.4, 0.95),

        "json": ("JSON Audit Artifacts", "Inventory, Tech, Structure", "square", 10.9, 3.8, 3.0, 1.3),

        "docs": ("project-documentation/", "35-Section Report Suite", "rect", 15.35, 5.4, 3.4, 1.2),
        "val": ("validate_report_evidence.py", "Anti-Hallucination Engine", "oval", 15.35, 2.2, 3.8, 1.3)
    }

    for node_id, (title, sub, shape_type, x, y, w, h) in nodes.items():
        if shape_type == "oval":
            patch = patches.Ellipse((x, y), w, h, ec='#09090b', fc='#ffffff', lw=2)
        elif shape_type == "square":
            patch = patches.Rectangle((x - w/2, y - h/2), w, h, ec='#09090b', fc='#f1f5f9', lw=2)
        else: # rect
            patch = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08",
                                          ec='#09090b', fc='#ffffff', lw=2)
        ax.add_patch(patch)
        ax.text(x, y + 0.12, title, color='#09090b', fontsize=9.5, fontweight='bold', ha='center', va='center')
        ax.text(x, y - 0.18, sub, color='#3f3f46', fontsize=8, ha='center', va='center')

    connections = [
        ("user", "skill"),
        ("skill", "inv"), ("skill", "tech"), ("skill", "struct"), ("skill", "sec"), ("skill", "evid"),
        ("inv", "json"), ("tech", "json"), ("struct", "json"), ("sec", "json"), ("evid", "json"),
        ("json", "docs"), ("docs", "val")
    ]

    for src_id, dst_id in connections:
        src = nodes[src_id]
        dst = nodes[dst_id]

        sx, sy, sw, sh = src[3], src[4], src[5], src[6]
        dx, dy, dw, dh = dst[3], dst[4], dst[5], dst[6]

        if abs(sx - dx) < 0.1:
            start = (sx, sy - sh/2) if sy > dy else (sx, sy + sh/2)
            end = (dx, dy + dh/2) if sy > dy else (dx, dy - dh/2)
        elif dx > sx:
            start = (sx + sw/2, sy)
            end = (dx - dw/2, dy)
        else:
            start = (sx - sw/2, sy)
            end = (dx + dw/2, dy)

        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="-|>", color='#09090b', lw=1.6,
                                    mutation_scale=13, connectionstyle="arc3,rad=0.0"))

    ax.set_xlim(0, 18.0)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    plt.title("System Architecture & Data Flow Diagram",
              color='#09090b', fontsize=15, pad=20, fontweight='bold')

    out_path = DIAGRAMS_DIR / "system_architecture.png"
    plt.savefig(out_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Rendered clean engineering architecture diagram to {out_path}")
    return out_path

def render_auth_flow_image():
    """Render a clean sequence pipeline diagram with white background, black text, and standard shapes."""
    fig, ax = plt.subplots(figsize=(13.5, 5.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    stages = [
        ("STAGE 1: INPUT SCAN", 0.5, 4.2),
        ("STAGE 2: AUDIT & REDACTION ENGINE", 4.6, 9.2),
        ("STAGE 3: SAFE OUTPUT", 9.6, 13.1)
    ]
    for title, x_min, x_max in stages:
        rect = patches.FancyBboxPatch((x_min, 0.4), x_max - x_min, 4.6, boxstyle="square,pad=0.15",
                                      ec='#cbd5e1', fc='#f8fafc', lw=1.2, linestyle='--')
        ax.add_patch(rect)
        ax.text((x_min + x_max)/2, 4.65, title, color='#475569', fontsize=9.5, fontweight='bold', ha='center', va='center')

    nodes = {
        "req": ("Codebase File Scan", "Raw Source Files & Configs", "oval", 2.35, 2.7, 3.2, 1.3),
        "sec": ("detect_secrets_safely.py", "Regex & Entropy Analyzer", "rect", 6.9, 3.6, 3.6, 1.2),
        "redact": ("Redaction Engine", "Masks API Keys & Tokens", "rect", 6.9, 1.8, 3.6, 1.2),
        "out": ("Safe Report Output", "Zero Exposed Secrets", "square", 11.35, 2.7, 3.0, 1.3)
    }

    for node_id, (title, sub, shape_type, x, y, w, h) in nodes.items():
        if shape_type == "oval":
            patch = patches.Ellipse((x, y), w, h, ec='#09090b', fc='#ffffff', lw=2)
        elif shape_type == "square":
            patch = patches.Rectangle((x - w/2, y - h/2), w, h, ec='#09090b', fc='#f1f5f9', lw=2)
        else: # rect
            patch = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.08",
                                          ec='#09090b', fc='#ffffff', lw=2)
        ax.add_patch(patch)
        ax.text(x, y + 0.12, title, color='#09090b', fontsize=10, fontweight='bold', ha='center', va='center')
        ax.text(x, y - 0.18, sub, color='#3f3f46', fontsize=8, ha='center', va='center')

    arrows = [
        ((3.95, 2.7), (5.1, 3.6)),
        ((3.95, 2.7), (5.1, 1.8)),
        ((8.7, 3.6), (9.85, 2.7)),
        ((8.7, 1.8), (9.85, 2.7))
    ]
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="-|>", color='#09090b', lw=1.6, mutation_scale=13))

    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 5.2)
    ax.axis('off')
    plt.title("Secret Audit & Automatic Redaction Pipeline Diagram",
              color='#09090b', fontsize=14, pad=15, fontweight='bold')

    out_path = DIAGRAMS_DIR / "authentication_flow.png"
    plt.savefig(out_path, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Rendered clean auth flow diagram to {out_path}")
    return out_path

def parse_md_content():
    """Parse PROJECT_RESEARCH_REPORT.md into structured sections and markdown elements."""
    text = MD_REPORT_PATH.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    sections = []
    current_section = None
    current_content = []

    for line in lines:
        if line.startswith("# "):
            continue
        elif line.startswith("## "):
            if current_section:
                sections.append((current_section, current_content))
            current_section = line[3:].strip()
            current_content = []
        else:
            if current_section is not None:
                current_content.append(line)

    if current_section:
        sections.append((current_section, current_content))

    return sections

def generate_full_docx_document(img_arch: Path, img_auth: Path):
    """Generate comprehensive DOCX document containing all 35 sections of the audit report."""
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Title Page
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("\n\nRepoLens Research Inspector\nFull Technical Research Audit Report")
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Exhaustive Codebase Audit, Technology Stack Ledger, Security Review & Architecture Documentation\n\n")
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph().add_run("-" * 55).font.color.rgb = RGBColor(203, 213, 225)

    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    data = [
        ("Repository Target:", "https://github.com/NLR-2007/inspect-repo.git"),
        ("Audited Branch / Commit:", "main / 84cd5ed6be3dcc22b9e3347034246bc5a505f99c"),
        ("Audit Date:", "2026-07-19"),
        ("Inspection Coverage:", "100% (22 Files Discovered / 22 Analyzed)"),
        ("Overall Production Score:", "56 / 100 (Grade D/F - Significant Hardening Required)"),
        ("Security Audit Status:", "PASSED (Zero exposed raw secrets; redaction fix required)")
    ]
    for idx, (k, v) in enumerate(data):
        row = table.rows[idx]
        row.cells[0].paragraphs[0].add_run(k).bold = True
        row.cells[1].paragraphs[0].add_run(v)

    doc.add_page_break()

    # Parse and add all 35 Sections
    sections = parse_md_content()

    for title, content_lines in sections:
        h = doc.add_heading(title, level=1)
        h.runs[0].font.color.rgb = RGBColor(30, 41, 59)

        # Insert Architecture Diagrams after section 13
        if "13. Architecture" in title and img_arch.exists():
            doc.add_paragraph("High-resolution architecture diagram rendering:")
            doc.add_picture(str(img_arch), width=Inches(6.5))
            p_cap = doc.add_paragraph("Figure 13.1: System Architecture & Data Flow Diagram")
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.runs[0].font.italic = True
            p_cap.runs[0].font.size = Pt(9)

        # Insert Auth Diagram after section 14
        if "14. Application Workflows" in title and img_auth.exists():
            doc.add_paragraph("High-resolution secret audit pipeline diagram rendering:")
            doc.add_picture(str(img_auth), width=Inches(6.5))
            p_cap2 = doc.add_paragraph("Figure 14.1: Secret Audit & Automatic Redaction Pipeline Diagram")
            p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap2.runs[0].font.italic = True
            p_cap2.runs[0].font.size = Pt(9)

        # Process Markdown Lines (Paragraphs, Tables, Bullet Points, Code Blocks)
        in_table = False
        table_rows = []

        for line in content_lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check Markdown Tables
            if "|" in line_str and ("---" in line_str or line_str.startswith("|")):
                if "---" in line_str:
                    continue # Skip separator line
                cells = [c.strip() for c in line_str.split("|")[1:-1]]
                table_rows.append(cells)
                in_table = True
                continue
            else:
                if in_table and table_rows:
                    # Flush table to document
                    t = doc.add_table(rows=len(table_rows), cols=max(len(r) for r in table_rows))
                    t.style = 'Table Grid'
                    for r_i, row in enumerate(table_rows):
                        for c_i, val in enumerate(row):
                            if c_i < len(t.rows[r_i].cells):
                                cell_p = t.rows[r_i].cells[c_i].paragraphs[0]
                                run = cell_p.add_run(val)
                                if r_i == 0:
                                    run.bold = True
                    table_rows = []
                    in_table = False

            # Check Bullet Lists
            if line_str.startswith("- ") or line_str.startswith("* "):
                p_bullet = doc.add_paragraph(style='List Bullet')
                p_bullet.add_run(line_str[2:].strip())
            elif line_str.startswith("```"):
                continue # Skip raw code fenced markers
            else:
                p_text = doc.add_paragraph(line_str)
                p_text.paragraph_format.space_after = Pt(4)

        if in_table and table_rows:
            t = doc.add_table(rows=len(table_rows), cols=max(len(r) for r in table_rows))
            t.style = 'Table Grid'
            for r_i, row in enumerate(table_rows):
                for c_i, val in enumerate(row):
                    if c_i < len(t.rows[r_i].cells):
                        cell_p = t.rows[r_i].cells[c_i].paragraphs[0]
                        run = cell_p.add_run(val)
                        if r_i == 0:
                            run.bold = True

    docx_path = DOCS_DIR / "PROJECT_RESEARCH_REPORT.docx"
    doc.save(str(docx_path))
    print(f"Generated complete 35-section DOCX document at {docx_path}")
    return docx_path

def generate_full_pdf_document(img_arch: Path, img_auth: Path):
    """Generate comprehensive PDF document containing all 35 sections of the audit report."""
    pdf_path = DOCS_DIR / "PROJECT_RESEARCH_REPORT.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter,
                            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,
        spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#64748b'),
        alignment=1,
        spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []

    # Title Page
    story.append(Spacer(1, 25))
    story.append(Paragraph("RepoLens Research Inspector", title_style))
    story.append(Paragraph("Full Technical Research & Architecture Audit Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=15))

    meta_data = [
        [Paragraph("<b>Repository Target:</b>", body_style), Paragraph("https://github.com/NLR-2007/inspect-repo.git", body_style)],
        [Paragraph("<b>Audited Branch / Commit:</b>", body_style), Paragraph("main / 84cd5ed6be3dcc22b9e3347034246bc5a505f99c", body_style)],
        [Paragraph("<b>Inspection Coverage:</b>", body_style), Paragraph("100% (22 Files Discovered / 22 Analyzed)", body_style)],
        [Paragraph("<b>Overall Score:</b>", body_style), Paragraph("56 / 100 (Grade D/F - Significant Hardening Required)", body_style)],
        [Paragraph("<b>Security Status:</b>", body_style), Paragraph("PASSED (Zero exposed raw secrets)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[150, 380])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # Add all 35 sections into PDF
    sections = parse_md_content()

    for title, content_lines in sections:
        story.append(Paragraph(title, h1_style))

        if "13. Architecture" in title and img_arch.exists():
            story.append(Spacer(1, 4))
            story.append(Image(str(img_arch), width=530, height=290))
            story.append(Paragraph("<i>Figure 13.1: System Architecture & Data Flow Diagram</i>", body_style))
            story.append(Spacer(1, 10))

        if "14. Application Workflows" in title and img_auth.exists():
            story.append(Spacer(1, 4))
            story.append(Image(str(img_auth), width=530, height=216))
            story.append(Paragraph("<i>Figure 14.1: Secret Audit & Automatic Redaction Pipeline Diagram</i>", body_style))
            story.append(Spacer(1, 10))

        in_table = False
        table_rows = []

        for line in content_lines:
            line_str = line.strip()
            if not line_str:
                continue

            if "|" in line_str and ("---" in line_str or line_str.startswith("|")):
                if "---" in line_str:
                    continue
                cells = [c.strip() for c in line_str.split("|")[1:-1]]
                table_rows.append(cells)
                in_table = True
                continue
            else:
                if in_table and table_rows:
                    t_cells = []
                    for r_idx, r in enumerate(table_rows):
                        row_p = [Paragraph(f"<b>{cell}</b>" if r_idx == 0 else cell, body_style) for cell in r]
                        t_cells.append(row_p)

                    num_cols = max(len(r) for r in t_cells)
                    col_w = 530 / max(num_cols, 1)
                    t = Table(t_cells, colWidths=[col_w] * num_cols)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
                        ('PADDING', (0,0), (-1,-1), 5),
                        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1'))
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 6))
                    table_rows = []
                    in_table = False

            if line_str.startswith("- ") or line_str.startswith("* "):
                bullet_text = f"• {line_str[2:].strip()}"
                story.append(Paragraph(bullet_text, body_style))
            elif line_str.startswith("```"):
                continue
            else:
                clean_text = line_str.replace("[", "").replace("]", "").replace("`", "")
                story.append(Paragraph(clean_text, body_style))

        if in_table and table_rows:
            t_cells = []
            for r_idx, r in enumerate(table_rows):
                row_p = [Paragraph(f"<b>{cell}</b>" if r_idx == 0 else cell, body_style) for cell in r]
                t_cells.append(row_p)

            num_cols = max(len(r) for r in t_cells)
            col_w = 530 / max(num_cols, 1)
            t = Table(t_cells, colWidths=[col_w] * num_cols)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
                ('PADDING', (0,0), (-1,-1), 5),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1'))
            ]))
            story.append(t)
            story.append(Spacer(1, 6))

    doc.build(story)
    print(f"Generated complete 35-section PDF document at {pdf_path}")
    return pdf_path

def main():
    print("Generating clean engineering diagram images and full 35-section Word (.docx) & PDF documents...")
    img_arch = render_system_architecture_image()
    img_auth = render_auth_flow_image()

    docx_path = generate_full_docx_document(img_arch, img_auth)
    pdf_path = generate_full_pdf_document(img_arch, img_auth)

    print("\nSUCCESS! Full 35-section Word (.docx) & PDF documents generated:")
    print(f" - Architecture Image: {img_arch}")
    print(f" - Auth Flow Image: {img_auth}")
    print(f" - Word Document: {docx_path}")
    print(f" - PDF Document: {pdf_path}")

if __name__ == "__main__":
    main()
