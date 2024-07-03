from typing import List, Literal
from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn
from pydantic import BaseModel, Field
from datetime import datetime
import os
from jinja2 import Template, Environment, FileSystemLoader


class Course(BaseModel):
    name: str
    grade: str
    credits: float

    @property
    def credits_str(self) -> str:
        return '{:.2f}'.format(round(self.credits, 2))


class Period(BaseModel):
    name: Literal['Fall', 'Winter']
    courses: List[Course]


class Year(BaseModel):
    name: str
    periods: List[Period] = Field(default_factory=list)
    total_credits: float = 0.0


class Student(BaseModel):
    name: str
    program: Literal['Advanced', 'Associate', 'Online']
    grade: str
    credits_earned: float
    gpa: float
    start_date: str
    expected_graduation: str
    years: List[Year]

    @property
    def gpa_str(self) -> str:
        return '{:.2f}'.format(round(self.gpa, 2))

    @property
    def credits_earned_str(self) -> str:
        return '{:.2f}'.format(round(self.credits_earned, 2))


app = FastAPI()
env = Environment(loader=FileSystemLoader('templates'))


@app.get("/")
def read_item():
    return {
        "app": "miftaah transcript generator",
        "version": "0.1.0",
        "description": "generate a transcript given a students info. see /docs for api usage"
    }


@app.post("/transcript")
async def generate_transcript(s: Student):
    today = datetime.now().strftime("%B %d, %Y")
    template = env.get_template('template.html')

    # Ensure both Fall and Winter periods are included for each year
    years = []
    for year in s.years:
        fall_periods = [period for period in year.periods if period.name == 'Fall']
        winter_periods = [period for period in year.periods if period.name == 'Winter']

        if not fall_periods:
            fall_periods.append(Period(name='Fall', courses=[]))
        if not winter_periods:
            winter_periods.append(Period(name='Winter', courses=[]))

        years.append({
            'year': year.name,
            'fall_periods': fall_periods,
            'winter_periods': winter_periods,
            'fall_total_credits': sum(course.credits for period in fall_periods for course in period.courses),
            'winter_total_credits': sum(course.credits for period in winter_periods for course in period.courses),
        })

    # Render the HTML using the provided data
    html_content = template.render(
        name=s.name,
        grade=s.grade,
        credits_earned_str=s.credits_earned_str,
        gpa_str=s.gpa_str,
        start_date=s.start_date,
        expected_graduation=s.expected_graduation,
        years=years,
        today=today
    )

    with open("input.html", "w+") as f:
        f.write(html_content)

    # Run the HTML to PDF conversion
    os.system("wkhtmltopdf --allow /app/images input.html result.pdf")

    # Return the PDF file as a StreamingResponse
    headers = {"Content-Disposition": "attachment; filename=result.pdf"}
    return StreamingResponse(open("result.pdf", "rb"), media_type="application/pdf", headers=headers)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
