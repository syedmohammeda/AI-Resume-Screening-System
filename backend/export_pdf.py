from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def export_to_pdf(results, filename="Candidate_Report.pdf"):

    pdf = SimpleDocTemplate(filename)

    data = [["Rank", "Candidate", "Email", "Score"]]

    for i, candidate in enumerate(results, start=1):
        data.append([
            i,
            candidate["name"],
            candidate["email"],
            f"{candidate['score']}%"
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige)
    ]))

    pdf.build([table])