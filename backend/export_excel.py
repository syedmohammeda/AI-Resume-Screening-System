from openpyxl import Workbook

def export_to_excel(results, filename="Candidate_Report.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Candidates"

    ws.append([
        "Rank",
        "Candidate",
        "Email",
        "Phone",
        "Skills",
        "Match Score"
    ])

    for i, candidate in enumerate(results, start=1):
        ws.append([
            i,
            candidate["name"],
            candidate["email"],
            candidate["phone"],
            ", ".join(candidate["skills"]),
            f"{candidate['score']}%"
        ])

    wb.save(filename)