from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

questions = [
    "What is your full name?",
    "Your email address?",
    "Your phone number?",
    "Your highest qualification?",
    "Your key skills (comma separated)?",
    "Your work experience (if any)?",
    "Your career objective?"
]

user_data = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    step = len(user_data)

    if step < len(questions):
        user_data[questions[step]] = user_msg

        # If last question answered → show resume
        if step == len(questions) - 1:
            return jsonify({"reply": format_resume()})

        return jsonify({"reply": questions[step + 1]})

    return jsonify({"reply": format_resume()})


def format_resume():
    return f"""
📄 RESUME

👤 Name: {user_data.get(questions[0], "")}
📧 Email: {user_data.get(questions[1], "")}
📞 Phone: {user_data.get(questions[2], "")}

🎓 Qualification:
{user_data.get(questions[3], "")}

🛠 Skills:
{user_data.get(questions[4], "")}

💼 Experience:
{user_data.get(questions[5], "")}

🎯 Career Objective:

{user_data.get(questions[6], "")}

⬇️ Click Download Resume button to get PDF
"""


# ✅ PDF DOWNLOAD ROUTE
@app.route("/download")
def download_resume():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "RESUME")

    c.setFont("Helvetica", 11)
    y = height - 100

    for key, value in user_data.items():
        c.drawString(50, y, f"{key}")
        y -= 15
        c.drawString(70, y, value)
        y -= 25

    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
