import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ─── AQA SUBJECT CODES ────────────────────────────────────────────────────────
# Format: "subject": { "papers": [(code, label, tier), ...], "spec": speccode }
# tier: "H"=Higher, "F"=Foundation, ""=no tier

AQA_GCSE = {
    "biology": {
        "code": "8461",
        "papers": [("84611","Paper 1","tiered"), ("84612","Paper 2","tiered")],
        "spec": "AQA-8461-SP-2016"
    },
    "chemistry": {
        "code": "8462",
        "papers": [("84621","Paper 1","tiered"), ("84622","Paper 2","tiered")],
        "spec": "AQA-8462-SP-2016"
    },
    "physics": {
        "code": "8463",
        "papers": [("84631","Paper 1","tiered"), ("84632","Paper 2","tiered")],
        "spec": "AQA-8463-SP-2016"
    },
    "combined science": {
        "code": "8464",
        "papers": [
            ("8464B1","Biology Paper 1","tiered"), ("8464B2","Biology Paper 2","tiered"),
            ("8464C1","Chemistry Paper 1","tiered"), ("8464C2","Chemistry Paper 2","tiered"),
            ("8464P1","Physics Paper 1","tiered"), ("8464P2","Physics Paper 2","tiered"),
        ],
        "spec": "AQA-8464-SP-2016"
    },
    "maths": {
        "code": "8300",
        "papers": [("83001","Paper 1","tiered"), ("83002","Paper 2","tiered"), ("83003","Paper 3","tiered")],
        "spec": "AQA-8300-SP-2015"
    },
    "mathematics": {
        "code": "8300",
        "papers": [("83001","Paper 1","tiered"), ("83002","Paper 2","tiered"), ("83003","Paper 3","tiered")],
        "spec": "AQA-8300-SP-2015"
    },
    "english language": {
        "code": "8700",
        "papers": [("87001","Paper 1",""), ("87002","Paper 2","")],
        "spec": "AQA-8700-SP-2015"
    },
    "english literature": {
        "code": "8702",
        "papers": [("87021","Paper 1",""), ("87022","Paper 2","")],
        "spec": "AQA-8702-SP-2015"
    },
    "geography": {
        "code": "8035",
        "papers": [("80351","Paper 1",""), ("80352","Paper 2",""), ("80353","Paper 3","")],
        "spec": "AQA-8035-SP-2016"
    },
    "history": {
        "code": "8145",
        "papers": [("81451A","Paper 1",""), ("81452N","Paper 2","")],
        "spec": "AQA-8145-SP-2016"
    },
    "computer science": {
        "code": "8525",
        "papers": [("85251","Paper 1",""), ("85252","Paper 2","")],
        "spec": "AQA-8525-SP-2020"
    },
    "religious studies": {
        "code": "8062",
        "papers": [("80621","Paper 1",""), ("80622","Paper 2","")],
        "spec": "AQA-8062-SP-2016"
    },
    "french": {
        "code": "8658",
        "papers": [("86581","Listening & Reading",""), ("86582","Speaking",""), ("86583","Writing","")],
        "spec": "AQA-8658-SP-2016"
    },
    "spanish": {
        "code": "8698",
        "papers": [("86981","Listening & Reading",""), ("86982","Speaking",""), ("86983","Writing","")],
        "spec": "AQA-8698-SP-2016"
    },
    "german": {
        "code": "8668",
        "papers": [("86681","Listening & Reading",""), ("86682","Speaking",""), ("86683","Writing","")],
        "spec": "AQA-8668-SP-2016"
    },
    "business": {
        "code": "8132",
        "papers": [("81321","Paper 1",""), ("81322","Paper 2","")],
        "spec": "AQA-8132-SP-2017"
    },
    "drama": {
        "code": "8261",
        "papers": [("82611","Paper 1",""), ("82612","Paper 2","")],
        "spec": "AQA-8261-SP-2016"
    },
    "music": {
        "code": "8271",
        "papers": [("82711","Paper 1","")],
        "spec": "AQA-8271-SP-2016"
    },
    "pe": {
        "code": "8582",
        "papers": [("85821","Paper 1",""), ("85822","Paper 2","")],
        "spec": "AQA-8582-SP-2016"
    },
    "physical education": {
        "code": "8582",
        "papers": [("85821","Paper 1",""), ("85822","Paper 2","")],
        "spec": "AQA-8582-SP-2016"
    },
    "food preparation and nutrition": {
        "code": "8585",
        "papers": [("85851","Paper 1","")],
        "spec": "AQA-8585-SP-2016"
    },
    "art and design": {
        "code": "8201",
        "papers": [],
        "spec": "AQA-8201-SP-2016"
    },
    "design and technology": {
        "code": "8552",
        "papers": [("85521","Paper 1","")],
        "spec": "AQA-8552-SP-2017"
    },
    "psychology": {
        "code": "8182",
        "papers": [("81821","Paper 1",""), ("81822","Paper 2","")],
        "spec": "AQA-8182-SP-2017"
    },
    "sociology": {
        "code": "8192",
        "papers": [("81921","Paper 1",""), ("81922","Paper 2","")],
        "spec": "AQA-8192-SP-2017"
    },
    "media studies": {
        "code": "8572",
        "papers": [("85721","Paper 1",""), ("85722","Paper 2","")],
        "spec": "AQA-8572-SP-2017"
    },
    "statistics": {
        "code": "8382",
        "papers": [("83821","Paper 1",""), ("83822","Paper 2","")],
        "spec": "AQA-8382-SP-2017"
    },
}

AQA_ALEVEL = {
    "biology": {
        "code": "7402",
        "papers": [("74021","Paper 1",""), ("74022","Paper 2",""), ("74023","Paper 3","")],
        "spec": "AQA-7401-7402-SP-2015"
    },
    "chemistry": {
        "code": "7405",
        "papers": [("74051","Paper 1",""), ("74052","Paper 2",""), ("74053","Paper 3","")],
        "spec": "AQA-7404-7405-SP-2015"
    },
    "physics": {
        "code": "7408",
        "papers": [("74081","Paper 1",""), ("74082","Paper 2",""), ("74083","Paper 3","")],
        "spec": "AQA-7407-7408-SP-2015"
    },
    "maths": {
        "code": "7357",
        "papers": [("73571","Paper 1",""), ("73572","Paper 2",""), ("73573","Paper 3","")],
        "spec": "AQA-7357-SP-2017"
    },
    "mathematics": {
        "code": "7357",
        "papers": [("73571","Paper 1",""), ("73572","Paper 2",""), ("73573","Paper 3","")],
        "spec": "AQA-7357-SP-2017"
    },
    "further maths": {
        "code": "7367",
        "papers": [("73671","Paper 1",""), ("73672","Paper 2",""), ("73673","Paper 3","")],
        "spec": "AQA-7366-7367-SP-2017"
    },
    "further mathematics": {
        "code": "7367",
        "papers": [("73671","Paper 1",""), ("73672","Paper 2",""), ("73673","Paper 3","")],
        "spec": "AQA-7366-7367-SP-2017"
    },
    "english language": {
        "code": "7702",
        "papers": [("77021","Paper 1",""), ("77022","Paper 2","")],
        "spec": "AQA-7701-7702-SP-2015"
    },
    "english literature": {
        "code": "7712",
        "papers": [("77121","Paper 1",""), ("77122","Paper 2",""), ("77123","Paper 3","")],
        "spec": "AQA-7711-7712-SP-2015"
    },
    "english language and literature": {
        "code": "7707",
        "papers": [("77071","Paper 1",""), ("77072","Paper 2","")],
        "spec": "AQA-7706-7707-SP-2015"
    },
    "geography": {
        "code": "7037",
        "papers": [("70371","Paper 1",""), ("70372","Paper 2",""), ("70373","Paper 3","")],
        "spec": "AQA-7037-SP-2016"
    },
    "history": {
        "code": "7042",
        "papers": [("71421N","Paper 1",""), ("71422N","Paper 2",""), ("71423","Paper 3","")],
        "spec": "AQA-7041-7042-SP-2015"
    },
    "psychology": {
        "code": "7182",
        "papers": [("71821","Paper 1",""), ("71822","Paper 2",""), ("71823","Paper 3","")],
        "spec": "AQA-7181-7182-SP-2015"
    },
    "sociology": {
        "code": "7192",
        "papers": [("71921","Paper 1",""), ("71922","Paper 2",""), ("71923","Paper 3","")],
        "spec": "AQA-7191-7192-SP-2015"
    },
    "economics": {
        "code": "7136",
        "papers": [("71361","Paper 1",""), ("71362","Paper 2",""), ("71363","Paper 3","")],
        "spec": "AQA-7135-7136-SP-2015"
    },
    "business": {
        "code": "7132",
        "papers": [("71321","Paper 1",""), ("71322","Paper 2",""), ("71323","Paper 3","")],
        "spec": "AQA-7131-7132-SP-2015"
    },
    "computer science": {
        "code": "7517",
        "papers": [("75171","Paper 1",""), ("75172","Paper 2","")],
        "spec": "AQA-7516-7517-SP-2015"
    },
    "politics": {
        "code": "7152",
        "papers": [("71521","Paper 1",""), ("71522","Paper 2",""), ("71523","Paper 3","")],
        "spec": "AQA-7151-7152-SP-2017"
    },
    "law": {
        "code": "7162",
        "papers": [("71621","Paper 1",""), ("71622","Paper 2",""), ("71623","Paper 3","")],
        "spec": "AQA-7161-7162-SP-2017"
    },
    "philosophy": {
        "code": "7172",
        "papers": [("71721","Paper 1",""), ("71722","Paper 2","")],
        "spec": "AQA-7171-7172-SP-2017"
    },
    "french": {
        "code": "7652",
        "papers": [("76521","Listening, Reading & Writing",""), ("76522","Speaking","")],
        "spec": "AQA-7651-7652-SP-2016"
    },
    "spanish": {
        "code": "7692",
        "papers": [("76921","Listening, Reading & Writing",""), ("76922","Speaking","")],
        "spec": "AQA-7691-7692-SP-2016"
    },
    "german": {
        "code": "7662",
        "papers": [("76621","Listening, Reading & Writing",""), ("76622","Speaking","")],
        "spec": "AQA-7661-7662-SP-2016"
    },
    "pe": {
        "code": "7582",
        "papers": [("75821","Paper 1",""), ("75822","Paper 2","")],
        "spec": "AQA-7581-7582-SP-2016"
    },
    "physical education": {
        "code": "7582",
        "papers": [("75821","Paper 1",""), ("75822","Paper 2","")],
        "spec": "AQA-7581-7582-SP-2016"
    },
    "media studies": {
        "code": "7572",
        "papers": [("75721","Paper 1",""), ("75722","Paper 2","")],
        "spec": "AQA-7571-7572-SP-2017"
    },
    "drama": {
        "code": "7262",
        "papers": [("72621","Paper 1",""), ("72622","Paper 2","")],
        "spec": "AQA-7261-7262-SP-2016"
    },
    "music": {
        "code": "7272",
        "papers": [("72721","Paper 1",""), ("72722","Paper 2","")],
        "spec": "AQA-7271-7272-SP-2016"
    },
    "religious studies": {
        "code": "7062",
        "papers": [("70621","Paper 1",""), ("70622","Paper 2","")],
        "spec": "AQA-7061-7062-SP-2016"
    },
    "environmental science": {
        "code": "7447",
        "papers": [("74471","Paper 1",""), ("74472","Paper 2",""), ("74473","Paper 3","")],
        "spec": "AQA-7446-7447-SP-2017"
    },
}

AQA_ASLEVEL = {
    "biology": {"code":"7401","papers":[("74011","Paper 1",""),("74012","Paper 2","")],"spec":"AQA-7401-7402-SP-2015"},
    "chemistry": {"code":"7404","papers":[("74041","Paper 1",""),("74042","Paper 2","")],"spec":"AQA-7404-7405-SP-2015"},
    "physics": {"code":"7407","papers":[("74071","Paper 1",""),("74072","Paper 2","")],"spec":"AQA-7407-7408-SP-2015"},
    "maths": {"code":"7356","papers":[("73561","Paper 1",""),("73562","Paper 2","")],"spec":"AQA-7356-SP-2017"},
    "mathematics": {"code":"7356","papers":[("73561","Paper 1",""),("73562","Paper 2","")],"spec":"AQA-7356-SP-2017"},
    "psychology": {"code":"7181","papers":[("71811","Paper 1",""),("71812","Paper 2","")],"spec":"AQA-7181-7182-SP-2015"},
    "economics": {"code":"7135","papers":[("71351","Paper 1",""),("71352","Paper 2","")],"spec":"AQA-7135-7136-SP-2015"},
    "history": {"code":"7041","papers":[("70411N","Paper 1",""),("70412N","Paper 2","")],"spec":"AQA-7041-7042-SP-2015"},
    "geography": {"code":"7036","papers":[("70361","Paper 1",""),("70362","Paper 2","")],"spec":"AQA-7037-SP-2016"},
}

YEARS = ["2024","2023","2022","2019","2018","2017"]
NOV_YEARS = ["2023","2022","2021","2020","2019","2018","2017"]
BASE = "https://filestore.aqa.org.uk/sample-papers-and-mark-schemes"
SPEC_BASE = "https://filestore.aqa.org.uk/resources"

def make_aqa_urls(level_dict, subject_key, resource_types):
    info = level_dict.get(subject_key)
    if not info:
        return []

    results = []
    papers = info["papers"]

    for paper_code, paper_label, tier in papers:
        if "paper" in resource_types:
            for year in YEARS:
                yy = year[2:]
                if tier == "tiered":
                    for t, tlabel in [("H","Higher"), ("F","Foundation")]:
                        results.append({
                            "title": f"AQA {paper_label} {tlabel} — June {year}",
                            "type": "paper",
                            "url": f"{BASE}/{year}/june/AQA-{paper_code}{t}-QP-JUN{yy}.PDF"
                        })
                        # November series
                        if year in NOV_YEARS:
                            results.append({
                                "title": f"AQA {paper_label} {tlabel} — November {year}",
                                "type": "paper",
                                "url": f"{BASE}/{year}/november/AQA-{paper_code}{t}-QP-NOV{yy}.PDF"
                            })
                else:
                    results.append({
                        "title": f"AQA {paper_label} — June {year}",
                        "type": "paper",
                        "url": f"{BASE}/{year}/june/AQA-{paper_code}-QP-JUN{yy}.PDF"
                    })
                    if year in NOV_YEARS:
                        results.append({
                            "title": f"AQA {paper_label} — November {year}",
                            "type": "paper",
                            "url": f"{BASE}/{year}/november/AQA-{paper_code}-QP-NOV{yy}.PDF"
                        })

        if "mark" in resource_types:
            for year in YEARS:
                yy = year[2:]
                if tier == "tiered":
                    for t, tlabel in [("H","Higher"), ("F","Foundation")]:
                        results.append({
                            "title": f"AQA {paper_label} {tlabel} Mark Scheme — June {year}",
                            "type": "mark",
                            "url": f"{BASE}/{year}/june/AQA-{paper_code}{t}-W-MS-JUN{yy}.PDF"
                        })
                else:
                    results.append({
                        "title": f"AQA {paper_label} Mark Scheme — June {year}",
                        "type": "mark",
                        "url": f"{BASE}/{year}/june/AQA-{paper_code}-W-MS-JUN{yy}.PDF"
                    })

    # Spec
    if "spec" in resource_types and info.get("spec"):
        # Try to guess the subject folder from the spec code
        subject_folder = subject_key.replace(" ", "-")
        results.append({
            "title": "AQA Specification",
            "type": "spec",
            "url": f"https://filestore.aqa.org.uk/resources/{subject_folder}/specifications/{info['spec']}.PDF"
        })

    return results


def get_papers(board, level, subject, resource_types):
    subject = subject.lower().strip()

    if board == "AQA":
        if level == "gcse":
            return make_aqa_urls(AQA_GCSE, subject, resource_types)
        elif level == "alevel":
            return make_aqa_urls(AQA_ALEVEL, subject, resource_types)
        elif level == "aslevel":
            return make_aqa_urls(AQA_ASLEVEL, subject, resource_types)

    return []


@app.route("/")
def index():
    # Build subject lists for each level for the dropdowns
    gcse_subjects = sorted(set(AQA_GCSE.keys()) - {"mathematics", "physical education", "further mathematics"})
    alevel_subjects = sorted(set(AQA_ALEVEL.keys()) - {"mathematics", "physical education", "further mathematics"})
    aslevel_subjects = sorted(set(AQA_ASLEVEL.keys()) - {"mathematics"})
    return render_template("index.html",
        gcse_subjects=gcse_subjects,
        alevel_subjects=alevel_subjects,
        aslevel_subjects=aslevel_subjects)


@app.route("/api/papers", methods=["POST"])
def papers():
    data = request.json
    board = data.get("board", "")
    level = data.get("level", "")
    subject = data.get("subject", "")
    resource_types = data.get("types", ["paper", "mark", "report", "spec"])

    results = get_papers(board, level, subject, resource_types)
    return jsonify({"papers": results, "total": len(results)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
