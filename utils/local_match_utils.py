from typing import List, Dict, Tuple
import re
import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config
)

prompt = """
Analyze the job description and classify each keyword as either high priority or low priority. High priority keywords, are those related to essential Technologies skills or experience directly mentioned in the job title or requirements, low priority keywords are those related to soft skills or general knowledge that are not directly mentioned.\nThe given examples of input are of job descriptions and the output are the response by ai model, which we want to achieve so try to get the response like these:\nDo not provide me input just give the high priority and low priority keywords\n\nAs we are doing it for Computer science engineeringjobs so make sure to put all the tech skills in high priority and soft skills and broader tech terms in low priority.

Examples:

input: [job description]:Job Title: MERN Full Stack Developer (Backend Heavy)Location: Bangalore, KarnatakaExperience Required: Minimum 3 YearsJob Type: Full-TimeAbout Us:We are a dynamic and innovative tech company focused on delivering high-quality software solutions across various industries. Our team thrives on solving complex challenges and creating impactful digital products. We are currently seeking a talented MERN Full Stack Developer with a backend-heavy focus to join our team and help build scalable, robust applications.Job Description:We are looking for a skilled MERN Full Stack Developer with a strong emphasis on backend development. The ideal candidate should have in-depth experience working with modern backend technologies and frameworks, with a solid understanding of database and system design. You will be responsible for designing, developing, and maintaining complex web applications, ensuring their responsiveness, performance, and scalability.Key Responsibilities:Develop and maintain scalable backend services using Node.js, Express, and Sequelize.Design and manage relational databases, primarily PostgreSQL, ensuring data integrity and performance optimization.Implement RESTful APIs and integrate with third-party services.Design, develop, and maintain front-end applications using React, React Native, Next.js, and Redux.Work with state management libraries such as React Query and Redux to handle data flows efficiently.Build and maintain real-time features using WebSockets.Containerize applications using Docker for development, testing, and production environments.Collaborate with DevOps teams to deploy applications on AWS or Google Cloud platforms.Participate in system design discussions and contribute to the architecture of new solutions.Write clean, maintainable, and efficient code while following best practices for software development.Conduct code reviews and provide constructive feedback to other developers.Troubleshoot, debug, and optimize existing applications for maximum speed and scalability.Ensure security and data protection measures are in place across all applications.Required Skills and Qualifications:Backend Technologies: Strong proficiency in Node.js, Express.js, Sequelize, and PostgreSQL.Frontend Technologies: Proficient in React, React Native, Next.js, and Redux.State Management: Experience with React Query, Redux, and other state management libraries.Real-time Communication: Experience with WebSockets and real-time communication libraries.Containerization: Proficiency in Docker for application containerization.Cloud Platforms: Experience deploying applications on AWS and/or Google Cloud.System and Database Design: Strong understanding of system design principles and database schema design.Version Control: Proficient in using Git and GitHub for version control.Additional Skills: Experience with microservices architecture, serverless computing, and CI/CD pipelines is a plus.Soft Skills: Excellent problem-solving skills, attention to detail, strong communication skills, and the ability to work in a team-oriented environment.Preferred Qualifications:Experience with other databases like MongoDB, Redis, or Cassandra.Familiarity with GraphQL and related technologies.Knowledge of TypeScript for better type safety and code maintainability.Experience with test-driven development (TDD) and automated testing frameworks.Familiarity with Agile methodologies and tools like JIRA or Trello.What We Offer:Competitive salary and benefits package.Flexible working hours and remote work options.Opportunities for professional development and career growth.Collaborative and inclusive work environment.Access to the latest technologies and tools.The chance to work on exciting and challenging projects.
output: High Priority Keywords: MongoDB, Agile, Git, React, Node.js, Redux, Cassandra, Docker, Google Cloud, GraphQL, Jira, Next.js, PostgreSQL, Redis, Serverless, Websockets, containerization, CI/CD, TypeScript.\nLow Priority Keywords: backend, database, microservices, front-end, automated testing, digital products, state management, full stack, TDD, version control, DevOps.

input: About the Job:We are looking for a highly skilled and motivated Backend Engineer with a strong proficiency in Python to join our dynamic team. This role involves designing, developing, and optimizing scalable backend solutions that support our cutting-edge platform. If you're passionate about building robust systems and thrive in collaborative environments, we want to hear from you!Skills Required:PythonDjango/FlaskDocker ContainersAWS Services (EC2, RDS, S3)RESTful API DevelopmentSQL & NoSQL DatabasesResponsibilities:Collaborate with teams to design backend architectures and APIs.Build, test, and deploy scalable backend services using Python frameworks.Ensure backend systems are secure, efficient, and reliable.Work with DevOps teams to manage cloud infrastructure.Stay updated on backend development trends and technologies.Qualifications:Bachelor's degree in Computer Science or equivalent.Proven backend development experience using Python.Familiarity with cloud platforms like AWS or GCP.Strong database management skills.Excellent problem-solving abilities.Join Securitic.AI and be part of our mission to create a better future through innovative technology solutions!
output: High Priority Keywords: Django, Python, SQL, backend, API, Docker, Flask, GCP, NoSQL, database, cloud infrastructure, DevOps.\nLow Priority Keyword: problem-solving.

input: About the jobWho are we and what do we do?BrowserStack is the world's leading software testing platform powering over two million tests every day across 19 global data centers. BrowserStack's products help developers build bug-free software for the 5 billion internet users accessing websites and mobile applications through millions of combinations of digital environments—devices, browsers, operating systems, and versions. We help Tesco, Shell, NVIDIA, Discovery, Wells Fargo, and over 50,000 customers deliver quality software at speed by moving testing to our Cloud. With BrowserStack, Dev and QA teams can move fast while delivering an amazing experience for every customer.BrowserStack was founded by Ritesh Arora and Nakul Aggarwal in 2011 with the vision of becoming the testing infrastructure for the internet. We recently secured $200 million in Series B funding at a $4 billion valuation in June 2021.At BrowserStack We Solve Real Problems—each Day Is a Unique Challenge And An Opportunity To Make a Difference. We Strive To Be Open, Transparent, And Collaborative, So No Feat Is Too Big To Achieve. BrowserStack Is An Extension Of Its People And a Place Where They Can Grow Both Professionally And Personally. To That Effect, We're Humbled To Be Recognized By Leading Organizations Around The WorldBrowserStack is Great Place to Work-Certified™ 2020-21Named "SaaS Startup of the Year" in 2022 by SaaSBOOMiRanked in Forbes Cloud 100 in 2021 - for the second timeFeatured in LinkedIn Top Startups India 2018Role In NutshellYou will design, develop, document, and support systems and applications that are used by a large number of developers. You will work in an agile engineering team and will plan and execute technical projects that will support business requirements. You will collaborate with engineers across teams to build, review and deliver scalable solutions for different use-casesLocation (Remote): This position requires candidates based in Mumbai or willing to relocate to Mumbai only.Desired ExperienceSoftware development or programming experience of 1 - 3 yearsof experience.Extensive experience with at least one language: Ruby, Nodejs, Python, Java, C/C++.Good knowledge of operating systems, databases and networking conceptsAbility to work on Windows and Linux platforms below the application layer, including file systems, kernels, custom installations, scripting, internal APIs, etcAbility to communicate effectively with employees in the company in both technical and non-technical rolesAggressive problem diagnosis and solving real-world problems effectively.Should have a startup mentality, high willingness to learn, and be hardworking and be able to work in a fast-paced environment.What will you do?You will design and develop systems and applications, with agility and quality at scale.You will take responsibility for end-to-end ownership of tasks from development to production.Also will help with the design, implementation, and launch of many key product features. Participate in a culture of code reviews and collaborating closely with other engineersDrive best practices and engineering improvementsFind solutions and solve issues around a variety of operating systems or programming languages
output: High Priority Keywords: Python, C++, Agile, Linux, NodeJS, Java, Ruby, end-to-end, product features, SaaS, operating systems.\nLow Priority Keyword: agility.

input: About the jobAbout Eqvista:At Eqvista, we are committed to driving innovation and excellence in our industry. We believe that technology is a key enabler of our success, and we are looking for a talented IT Developer to join our dynamic team. We want to hear from you if you are passionate about technology, leadership, and strategic planning!Eqvista stands out as a comprehensive solution for entrepreneurs looking to manage their company's equity efficiently. With its array of features tailored to meet the needs of startups and growing businesses, it simplifies complex tasks associated with share management and compliance.Please visit: https://eqvista.com/ to learn more about our company.For more open position, please visit: https://eqvista.com/careers/Job Description:As a Junior Software Engineer, you will work closely with our experienced development team to design, develop, and maintain software applications. You will have the opportunity to learn from industry professionals, gain hands-on experience, and contribute to real-world projects.Responsibilities: Collaborate with team members to design and implement software solutions.Write clean, maintainable, and efficient code.Participate in code reviews and contribute to team best practices.Assist in troubleshooting and debugging applications.Stay up-to-date with emerging technologies and industry trends.Contribute to documentation and user manuals.Qualifications:Bachelor's degree in Computer Science, Software Engineering, or a related field (or equivalent experience).Familiarity with programming languages such as Java, Python, C#, or JavaScript.Basic understanding of web technologies (HTML, CSS, JavaScript) and frameworks (React, Angular, etc.) is a plus.Knowledge of database management systems (SQL or NoSQL).Strong problem-solving skills and attention to detail.Excellent communication and teamwork abilities.
output: High Priority Keywords: Python, SQL, Angular, React, NoSQL, C#, Java, JavaScript, HTML, database, strategic planning, troubleshooting, compliance.\nLow Priority Keywords: problem-solving, attention to detail.

input: About the jobLocation: RemoteAbout UsAt WorkSaga, we help employees log their work easily, making them aware of their accomplishments and aiding them in their career journey. We will share more information during the interview as this is currently in the Stealth Mode.Role DescriptionThis is a full-time remote role for a Python full-stack engineer at WorkSaga. You will be responsible for supporting the development and implementation of python web services & implement generative AI models and algorithms. You will work closely with senior team members to contribute to research projects, assist in data collection and annotation, and collaborate on model training and evaluation. This is a great opportunity to gain hands-on experience in the field of generative AI and contribute to cutting-edge research in artificial intelligence.QualificationsFinished or studying a Bachelor's or Master's degree in Computer Science, Engineering, or a related fieldStrong programming skills in Python and Web frameworks such as FastAPI, Flask or DjangoAtleast have 1-2 year of industry experienceExcellent problem-solving and analytical skillsStrong written and verbal communication skillsAbility to work independently and collaboratively in a team environmentKnowledge with SQL databases. Ideally MySQLExcellent programming skillsOur OfferComplete home-based positionBi-monthly online team event18 paid holidays, 15 sick dats and 12 national holidaysApplication ProcessForemost: Follow the instructions below to apply.Submit your detailed resume/CV highlighting your relevant experience and recent projects.Provide links to any applicable portfolio pieces or code samples, with a preference for Github profile.Detail your most recent projects where you extensively utilized PythonWe value your time and aim to respond to qualified candidates within 3 business days.Excited? Next steps (How to Apply):If you're ready to dive into the world of Python & AI, send us your simple and snazzy resume along with a quick note about why you're excited to join Worksaga.Click on easy apply confirming whether you filled the application using above link.Attached resumeImportant: We accept job applications only with the above form and confirmation with LinkedIn to make sure that you have read the post and is actually interested in the role.Process:We receive your applicationWe will invite you for an interview (if we like your Motivation and CV). Don't miss out on motivationThere will be just one interview with the hiring manager [Get-to-know & Technical Interview (coding & theory)]We will take 2-3 working days to replyWorkSaga is an equal opportunity employer. We welcome and encourage applicants from all backgrounds, including underrepresented groups, to apply.
output: High Priority Keywords: MySQL, Django, GitHub, Python, SQL, FastAPI, Flask, full-stack, web services.\nLow Priority Keywords: problem-solving, communication skills, verbal communication, written and verbal communication skills.
"""

def categorize_keywords(job_description: str) -> Tuple[List[str], List[str]]:
    """
    Categorize keywords from a job description into high and low priority using Gemini AI.
    Returns a tuple of (high_priority_keywords, low_priority_keywords)
    """
    response = model.generate_content(prompt + "\ninput: " + job_description)
    response_text = response.text

    # Extract high and low priority keywords from the response
    try:
        high_priority = []
        low_priority = []
        
        if "High Priority Keywords:" in response_text and "Low Priority Keywords:" in response_text:
            high_part = response_text.split("High Priority Keywords:")[1].split("Low Priority Keywords:")[0].strip()
            low_part = response_text.split("Low Priority Keywords:")[1].strip()
            
            high_priority = [k.strip() for k in high_part.split(",") if k.strip()]
            low_priority = [k.strip() for k in low_part.split(",") if k.strip()]
            
            # Remove any periods from the end of keywords
            high_priority = [k.rstrip(".") for k in high_priority]
            low_priority = [k.rstrip(".") for k in low_priority]
        
        return high_priority, low_priority
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return [], []

def calculate_keyword_match_score(job_description: str, resume_text: str, keywords: List[str]) -> float:
    """
    Calculate the percentage of keywords from job description found in resume
    """
    resume_text = resume_text.lower()
    matched_keywords = 0
    
    for keyword in keywords:
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', resume_text):
            matched_keywords += 1
    
    return round((matched_keywords / len(keywords)) * 100, 1) if keywords else 0

def calculate_technical_skills_match_score(job_description: str, resume_text: str) -> float:
    """
    Calculate technical skills match score using only high priority keywords from Gemini
    """
    high_priority, _ = categorize_keywords(job_description)
    
    if not high_priority:
        return 0.0
        
    return calculate_keyword_match_score(job_description, resume_text, high_priority)

def get_keyword_matches(keywords: List[str], resume_text: str) -> Dict[str, bool]:
    """
    Get a dictionary of keywords and whether they match in the resume
    """
    matches = {}
    resume_text = resume_text.lower()
    
    for keyword in keywords:
        matches[keyword] = bool(re.search(r'\b' + re.escape(keyword.lower()) + r'\b', resume_text))
    
    return matches
