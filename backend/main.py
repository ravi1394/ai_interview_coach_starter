from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from resume_parser import extract_text_from_pdf, generate_questions

import tempfile

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


app = FastAPI(title="AI Interview Coach")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Store interview session

interview_data = {

    "questions": [],

    "answers": [],

    "current": 0

}


# Model

class Answer(BaseModel):

    question: str

    answer: str


# Home API

@app.get("/")
def home():

    return {

        "message":

        "AI Interview Coach API Running"

    }


# Upload Resume

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):

    contents = await file.read()


    with tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    ) as temp:

        temp.write(contents)

        pdf_path = temp.name


    resume_text = extract_text_from_pdf(

        pdf_path

    )


    questions = generate_questions(

        resume_text

    )


    interview_data["questions"] = questions

    interview_data["answers"] = []

    interview_data["current"] = 0


    return {

        "filename":

        file.filename,


        "resume_text":

        resume_text[:1000],


        "questions":

        questions

    }


# Start Interview

@app.post("/start_interview")
def start_interview():

    if len(interview_data["questions"]) == 0:

        return {

            "message":

            "Upload Resume First"

        }


    interview_data["current"] = 0


    return {

        "question":

        interview_data["questions"][0]

    }


# Submit Answer

@app.post("/submit_answer")
def submit_answer(data: Answer):


    interview_data["answers"].append(

        {

            "question":

            data.question,


            "answer":

            data.answer

        }

    )


    interview_data["current"] += 1


    if interview_data["current"] < len(

        interview_data["questions"]

    ):


        return {

            "next_question":

            interview_data["questions"][

                interview_data["current"]

            ]

        }


    return {

        "message":

        "Interview Completed"

    }


# Evaluate Answer

@app.post("/evaluate")
def evaluate(data: Answer):


    words = len(

        data.answer.split()

    )


    if words > 50:

        score = 10


    elif words > 40:

        score = 8


    elif words > 25:

        score = 6


    elif words > 10:

        score = 4


    else:

        score = 2


    return {

        "score":

        score,


        "technical_score":

        score,


        "communication_score":

        min(score + 1, 10),


        "confidence_score":

        max(score - 1, 1),


        "feedback":

        "Use more examples and explain your approach clearly."

    }


# Dashboard

@app.get("/dashboard")
def dashboard():

    total_words = 0


    for ans in interview_data["answers"]:


        total_words += len(

            ans["answer"].split()

        )


    overall_score = min(

        10,

        max(

            1,

            total_words // 20

        )

    )


    return {


        "questions_attempted":

        len(

            interview_data["answers"]

        ),


        "overall_score":

        overall_score,


        "strengths": [

            "Problem Solving",

            "Communication"

        ],


        "weaknesses": [

            "Confidence",

            "Answer Structure"

        ]

    }


# Download PDF Report

@app.get("/download_report")
def download_report():

    doc = SimpleDocTemplate(

        "report.pdf"

    )


    styles = getSampleStyleSheet()


    story = []


    story.append(

        Paragraph(

            "AI Interview Report",

            styles['Title']

        )

    )


    story.append(

        Spacer(1, 25)

    )


    story.append(

        Paragraph(

            f"<b>Questions Attempted:</b> "

            f"{len(interview_data['answers'])}",

            styles['Normal']

        )

    )


    story.append(

        Spacer(1,20)

    )


    for item in interview_data["answers"]:


        story.append(

            Paragraph(

                f"<b>Question:</b> "

                f"{item['question']}",

                styles['Normal']

            )

        )


        story.append(

            Paragraph(

                f"<b>Answer:</b> "

                f"{item['answer']}",

                styles['Normal']

            )

        )


        story.append(

            Spacer(1,15)

        )


    story.append(

        Paragraph(

            "<b>Strengths:</b> "

            "Problem Solving, Communication",

            styles['Normal']

        )

    )


    story.append(

        Paragraph(

            "<b>Weaknesses:</b> "

            "Confidence, Answer Structure",

            styles['Normal']

        )

    )


    doc.build(story)


    return FileResponse(

        "report.pdf",

        media_type="application/pdf",

        filename="Interview_Report.pdf"

    )