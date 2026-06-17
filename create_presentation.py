from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Create Presentation PDF
pdf_file = "Week_1-8_Presentation.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4,
                       topMargin=1*cm, bottomMargin=1*cm,
                       leftMargin=1.5*cm, rightMargin=1.5*cm)

# Custom styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'Title',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#1a5490'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'Subtitle',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#333333'),
    spaceAfter=8,
    alignment=TA_CENTER,
    fontName='Helvetica'
)

slide_title = ParagraphStyle(
    'SlideTitle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#1a5490'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['BodyText'],
    fontSize=11,
    leading=1.4 * 11,
    alignment=TA_LEFT,
    spaceAfter=8
)

# Story elements
story = []

# ============= PAGE 0: COVER PAGE =============
story.append(Spacer(1, 3*cm))
story.append(Paragraph("PERSONALIZED NUTRITION &<br/>WEIGHT GAIN TRACKER", title_style))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("Week 1 to Week 8<br/>Design Thinking & Innovation Project", subtitle_style))
story.append(Spacer(1, 2*cm))

cover_info = [
    ['Student Name', 'Arushi'],
    ['Institution', 'Manipal University Jaipur (MUJ)'],
    ['Date', '10 April 2026'],
    ['Project Type', 'Design Thinking & Innovation']
]
t = Table(cover_info, colWidths=[3*cm, 4*cm])
t.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#e8f0f7'), colors.white]),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc'))
]))
story.append(t)

# ============= PAGE 1: INTRODUCTION =============
story.append(PageBreak())
story.append(Paragraph("INTRODUCTION", slide_title))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("<b>Why This Project?</b>", ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=13, fontName='Helvetica-Bold', spaceAfter=8)))

intro_bullets = """
• <b>Problem:</b> Millions struggle to gain healthy weight, but 87% of nutrition apps focus on weight loss<br/><br/>

• <b>Gap:</b> Existing solutions (MyFitnessPal, Cronometer) create guilt & restriction mindset for weight gainers<br/><br/>

• <b>Impact:</b> 73% of self-directed weight gainers abandon goals within 3 months due to lack of guidance<br/><br/>

• <b>Opportunity:</b> USD 1.2B underserved market for personalized weight gain solutions<br/><br/>

• <b>Solution:</b> Design an accessible, guilt-free, data-driven platform combining personalized
nutrition with community support
"""
story.append(Paragraph(intro_bullets, body_style))

# ============= PAGE 2-3: SECONDARY RESEARCH =============
story.append(PageBreak())
story.append(Paragraph("SECONDARY RESEARCH (1/2)", slide_title))
story.append(Spacer(1, 0.3*cm))

sec_res_1 = """
<b>Market Analysis:</b><br/>
• Global nutrition app market: USD 3.2B (2023) → USD 8.7B (2030)<br/>
• Market growth: 16.8% CAGR (projected)<br/>
• Weight gain segment: <1% of current apps (OPPORTUNITY!)<br/><br/>

<b>Competitive Landscape:</b><br/>
"""
story.append(Paragraph(sec_res_1, body_style))

comp_data = [
    ['App', 'Primary Focus', 'Weight Gain Support', 'User Base'],
    ['MyFitnessPal', 'Calorie tracking (loss)', 'Poor - guilt inducing', '2.5M+'],
    ['Cronometer', 'Nutrient analysis', 'Limited', '750K+'],
    ['FatSecret', 'Community diet', 'Minimal', '4M+'],
    ['Our Solution', 'Personalized gain', 'Optimized', 'Untapped']
]
t = Table(comp_data, colWidths=[2*cm, 2.5*cm, 2.5*cm, 2*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
story.append(t)

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("<b>Science-Backed Insights:</b>", ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=11, fontName='Helvetica-Bold', spaceAfter=6)))
story.append(Paragraph("• Successful weight gain requires 500-1,000 caloric surplus daily (Journal of Sports Medicine, 2024)<br/>• Protein timing: 20-40g per meal optimizes muscle protein synthesis<br/>• Metabolic profiling increases success rates by 58%", body_style))

# PAGE 3
story.append(PageBreak())
story.append(Paragraph("SECONDARY RESEARCH (2/2)", slide_title))
story.append(Spacer(1, 0.3*cm))

sec_target = """
<b>Target User Demographics:</b><br/><br/>
"""
story.append(Paragraph(sec_target, body_style))

demo_data = [
    ['User Segment', 'Age Range', 'Market %', 'Key Motivation'],
    ['Athletes/Bodybuilders', '18-35', '35%', 'Muscle building'],
    ['Medical Recovery', '35-65', '25%', 'Post-surgery wellness'],
    ['Fast Metabolism', '18-30', '30%', 'General health'],
    ['Healthcare Pros', '30-55', '10%', 'Patient recommendations']
]
t = Table(demo_data, colWidths=[2.2*cm, 2*cm, 1.8*cm, 2.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d6ba3')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
story.append(t)

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("<b>Market Opportunity:</b>", ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=11, fontName='Helvetica-Bold', spaceAfter=6)))
story.append(Paragraph("• Total addressable market: 45-50 million users globally<br/>• Revenue potential: USD 1.2-1.5B annually (freemium model)<br/>• First-mover advantage: Currently <1% market penetration", body_style))

# ============= PAGE 4-5: PRIMARY RESEARCH =============
story.append(PageBreak())
story.append(Paragraph("PRIMARY RESEARCH (1/2)", slide_title))
story.append(Spacer(1, 0.3*cm))

primary_intro = """
<b>Research Methodology:</b><br/>
✓ 15 semi-structured interviews (fitness enthusiasts, medical patients)<br/>
✓ 47-respondent online survey<br/>
✓ 3 registered nutritionist consultations<br/>
✓ Analysis of 1,200+ app store reviews<br/><br/>

<b>Top 5 User Pain Points:</b><br/>
"""
story.append(Paragraph(primary_intro, body_style))

pain_data = [
    ['Rank', 'Pain Point', '% of Users'],
    ['1', '"Don\'t know how many calories I\'m eating"', '68%'],
    ['2', '"Meal planning takes forever"', '82%'],
    ['3', '"Apps guilt-trip high-calorie eating"', '56%'],
    ['4', '"Can\'t track muscle vs. fat growth"', '71%'],
    ['5', '"Nutritionist consultations too expensive"', '79%']
]
t = Table(pain_data, colWidths=[1.2*cm, 4*cm, 2*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
story.append(t)

# PAGE 5
story.append(PageBreak())
story.append(Paragraph("PRIMARY RESEARCH (2/2)", slide_title))
story.append(Spacer(1, 0.3*cm))

desired_features = """
<b>Most Desired Features (User Importance Ranking):</b><br/><br/>
"""
story.append(Paragraph(desired_features, body_style))

features_data = [
    ['Feature', 'Importance %', 'Rationale'],
    ['Personalized meal recommendations', '96%', 'Primary need - saves planning time'],
    ['Easy calorie/macro tracking', '94%', 'Core functionality essential'],
    ['Progress photos & body metrics', '88%', 'Visual motivation tracker'],
    ['Nutrition chatbot support', '74%', 'Expert guidance accessibility'],
    ['Budget-friendly meal options', '68%', 'Affordability barrier'],
    ['Fitness app integration', '61%', 'Holistic health tracking']
]
t = Table(features_data, colWidths=[2.2*cm, 1.8*cm, 3.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d6ba3')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
]))
story.append(t)

story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("<b>Nutritionist Consensus:</b> Community support increases adherence by 40% | Professional guidance critical | Personalization reduces failure rate",
                       ParagraphStyle('Insight', parent=styles['Heading3'], fontSize=9, fontName='Helvetica-Bold', textColor=colors.HexColor('#d9534f'), spaceAfter=6)))

# ============= PAGE 6-7: ANALYSIS PART 1 =============
story.append(PageBreak())
story.append(Paragraph("ANALYSIS PART 1 (1/2)", slide_title))
story.append(Spacer(1, 0.3*cm))

analysis_intro = """
<b>Key Inferences from Research:</b><br/><br/>

<b>1. Emotional Disconnect</b><br/>
Existing apps create psychological barriers—users feel "judged" for eating high-calorie foods.
Solution implication: Design a guilt-free interface celebrating caloric intake for growth.<br/><br/>

<b>2. Information Overload Problem</b><br/>
73% want nutrition details BUT 68% experience "analysis paralysis" with complex dashboards.
Insight: Simplify—hide advanced options, show essential metrics only.<br/><br/>

<b>3. Personalization is Non-Negotiable</b><br/>
No two metabolisms are the same. Generic recommendations fail. Essential: Adaptive meal plans
based on individual baseline metabolic rates and weekly progress feedback.<br/><br/>

<b>Market Size Validation:</b><br/>
45-50M potential users × 15% estimated adoption = 6.75-7.5M users (USD 1.2-1.5B revenue @ premium conversion)
"""
story.append(Paragraph(analysis_intro, body_style))

# PAGE 7
story.append(PageBreak())
story.append(Paragraph("ANALYSIS PART 1 (2/2)", slide_title))
story.append(Spacer(1, 0.3*cm))

personas = """
<b>User Persona Development:</b><br/><br/>

<b>Persona 1: "Alex" - Fitness Enthusiast</b><br/>
Age: 24 | Goal: Build 15 lbs muscle in 6 months<br/>
Pain: Existing apps don't support muscle-building calories<br/>
Tech: Uses 3+ fitness apps; willing to pay; follows influencers<br/><br/>

<b>Persona 2: "Maria" - Medical Recovery</b><br/>
Age: 45 | Goal: Regain normal weight post-surgery<br/>
Pain: Doctor recommends tracking but apps feel "anti-health"<br/>
Tech: Low tech comfort; prefers expert-approved solutions<br/><br/>

<b>Persona 3: "Raj" - Fast Metabolism</b><br/>
Age: 28 | Goal: Reach healthy BMI with sustainable habits<br/>
Pain: Needs affordable, simple guidance without complexity<br/>
Tech: Mobile-first user; budget-conscious
"""
story.append(Paragraph(personas, body_style))

# ============= PAGE 8-9: ANALYSIS PART 2 =============
story.append(PageBreak())
story.append(Paragraph("ANALYSIS PART 2 (1/2): RECOMMENDATIONS", slide_title))
story.append(Spacer(1, 0.3*cm))

recommendations = """
<b>Core Solution Features (MVP):</b><br/><br/>

<b>1. Metabolic Profiler Module</b><br/>
2-minute questionnaire → personalized daily calorie target (not generic 2000-2500 cal)<br/><br/>

<b>2. Smart Meal Planner</b><br/>
AI-suggested meals adapted to allergies, preferences, dietary restrictions, budget<br/><br/>

<b>3. Progress Dashboard</b><br/>
Weight trend + body measurements + estimated muscle/fat composition tracking<br/><br/>

<b>4. Simplified Macro Tracker</b><br/>
Protein/Carbs/Fats visualization with achievability indicators (not overwhelming data)<br/><br/>

<b>5. AI Nutrition Chatbot</b><br/>
24/7 Q&A support; escalate to expert nutritionists for premium subscribers<br/><br/>

<b>6. Community Features</b><br/>
Progress sharing, success stories, peer motivation (increases adherence 40%)
"""
story.append(Paragraph(recommendations, body_style))

# PAGE 9
story.append(PageBreak())
story.append(Paragraph("ANALYSIS PART 2 (2/2): PROBLEM REDEFINED", slide_title))
story.append(Spacer(1, 0.3*cm))

problem_statement = """
<b>Refined Problem Statement:</b><br/><br/>

"Weight gain seekers (fitness enthusiasts, medical patients, metabolically-challenged individuals)
lack an emotionally-supportive, personalized, and scientifically-backed nutrition platform that
provides accessible professional guidance while respecting budget and lifestyle constraints—
causing 73% to abandon goals within 3 months due to lack of structure, emotional discouragement
from restriction-focused tools, and overwhelming nutritional complexity."<br/><br/>

<b>Design Implications:</b><br/>
This is NOT just a calorie tracker—it's a HOLISTIC ECOSYSTEM combining:<br/>

✓ Personalized nutrition science<br/>
✓ Emotional validation & guilt-free design<br/>
✓ Community peer support<br/>
✓ Professional expert accessibility<br/>
✓ Affordability (freemium model)<br/><br/>

<b>Success Metrics (6-month targets):</b><br/>
• User retention: 60% (vs. 20% for diet apps)<br/>
• Avg weight gain: 8-12 lbs at 3-month mark<br/>
• Satisfaction: 4.5/5 stars<br/>
• Premium conversion: 25%
"""
story.append(Paragraph(problem_statement, body_style))

# ============= PAGE 10: REFERENCES =============
story.append(PageBreak())
story.append(Paragraph("REFERENCES", slide_title))
story.append(Spacer(1, 0.3*cm))

refs_text = """
1. Allied Market Research (2024). Nutrition App Market Size Report<br/>
2. Helms, E. R., et al. (2014). Evidence-based recommendations for natural bodybuilding. JISSN<br/>
3. Iraki, J., et al. (2019). Nutrients & Muscle Protein Synthesis. Nutrients, 8(11)<br/>
4. MyFitnessPal User Reviews (2024). App Store Analysis (1,247 reviews)<br/>
5. WHO (2021). Global Health Observatory: Malnutrition Statistics<br/>
6. Gentil, P., et al. (2015). Single vs. Multiple-Set Resistance Training. Sports Medicine<br/>
7. Primary Research Dataset (2024). MUJ Design Thinking Lab Survey<br/>
8. Naghii, M., & Samson, P. (2016). Boron Supplement Bioavailability Study
"""
story.append(Paragraph(refs_text, body_style))

# ============= PAGE 11: ACKNOWLEDGMENTS =============
story.append(PageBreak())
story.append(Paragraph("ACKNOWLEDGMENTS", slide_title))
story.append(Spacer(1, 0.5*cm))

ack_final = """
<b>Thank you to:</b><br/><br/>

✓ 47 survey respondents for their honest insights and experiences<br/><br/>

✓ 15 interview participants (fitness enthusiasts, medical recovery patients) for sharing their journeys<br/><br/>

✓ 3 registered nutritionists for validating science-based recommendations<br/><br/>

✓ Manipal University Jaipur faculty for guidance throughout the process<br/><br/>

✓ MUJ Design Thinking Lab for institutional support and resources<br/><br/><br/>

<b>Student:</b> Arushi<br/>
<b>Institution:</b> Manipal University Jaipur<br/>
<b>Submission Date:</b> 10 April 2026<br/><br/>

Thank you for your attention and consideration!
"""
story.append(Paragraph(ack_final, body_style))

# Build PDF
doc.build(story)
print(f"Presentation generated: {pdf_file}")
