import pdfplumber


def extract_text_from_pdf(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text




def generate_questions(resume_text):

    questions = []

    text = resume_text.lower()



    # Java

    if "java" in text:

        questions.extend([

            "What is JVM?",

            "Explain OOP concepts in Java.",

            "Difference between ArrayList and LinkedList?",

            "What is Exception Handling in Java?"

        ])



    # Python

    if "python" in text:

        questions.extend([

            "What are Python decorators?",

            "Difference between list and tuple.",

            "Explain generators in Python.",

            "What is async programming in Python?"

        ])



    # FastAPI

    if "fastapi" in text:

        questions.extend([

            "Why did you choose FastAPI?",

            "How does FastAPI handle asynchronous requests?",

            "Explain dependency injection in FastAPI.",

            "How would you deploy a FastAPI application?"

        ])



    # Django

    if "django" in text:

        questions.extend([

            "Explain MVT architecture.",

            "What are Django Models?",

            "How does Django ORM work?",

            "Difference between Django and FastAPI."

        ])



    # Microservices

    if "microservices" in text:

        questions.extend([

            "What are microservices?",

            "Advantages of microservices over monolithic architecture.",

            "How do microservices communicate?",

            "What challenges did you face while implementing microservices?"

        ])



    # CI/CD

    if "ci/cd" in text or "ci cd" in text:

        questions.extend([

            "What is CI/CD?",

            "Explain the CI/CD pipeline.",

            "How would you automate deployment?",

            "What is the difference between CI and CD?"

        ])



    # Machine Learning

    if "machine learning" in text:

        questions.extend([

            "Explain Random Forest.",

            "Difference between supervised and unsupervised learning.",

            "What metrics do you use for model evaluation?",

            "Explain overfitting and underfitting."

        ])



    # Projects

    if "project" in text:

        questions.extend([

            "Explain your most challenging project.",

            "What problems did you solve in your project?",

            "What was your role in the project?",

            "What would you improve if given more time?"

        ])



    # System Design

    if "system design" in text:

        questions.extend([

            "How would you design a URL shortener?",

            "Explain load balancing.",

            "What is caching?",

            "Difference between SQL and NoSQL."

        ])



    # HR Questions

    questions.extend([

        "Tell me about yourself.",

        "What are your strengths?",

        "What are your weaknesses?",

        "Why should we hire you?",

        "Where do you see yourself in 5 years?",

        "Why do you want to join our company?"

    ])



    # Remove duplicates

    questions = list(dict.fromkeys(questions))



    return questions