# scripts/seed.py
import click

from app import create_app
from app.extensions import db
from app.models import User, Club


@click.command()
def seed():
    """Seed the database with initial Users and Clubs using the 10-tag vocab."""
    app = create_app()

    with app.app_context():
        # Clear existing data (development only)
        db.session.query(User).delete()
        db.session.query(Club).delete()
        db.session.commit()

        # ------------------------------------------------------------------
        # Users
        # interests must be a comma-separated list of TAG_VOCAB entries:
        # academic_stem_tech, business_career, creative_arts, sports,
        # gaming, service, activism_environment, politics, cultural, faith
        # ------------------------------------------------------------------
        users = [
            User(
                email="alice@example.com",
                name="Alice",
                year="freshman",
                major="Computer Science",
                # Alice is into tech, gaming and a bit of creative things
                interests="academic_stem_tech,gaming,creative_arts",
            ),
            User(
                email="bob@example.com",
                name="Bob",
                year="sophomore",
                major="Economics",
                # Bob is more business and career oriented, but also social
                interests="business_career,service,cultural",
            ),
            User(
                email="carol@example.com",
                name="Carol",
                year="junior",
                major="Environmental Science",
                # Carol cares about environment / activism and outdoors
                interests="activism_environment,sports,service",
            ),
            User(
                email="dave@example.com",
                name="Dave",
                year="freshman",
                major="Undeclared",
                # Dave is mainly social / gaming / casual sports
                interests="gaming,sports,cultural",
            ),
        ]

        # ------------------------------------------------------------------
        # Clubs
        # tags must also be comma-separated TAG_VOCAB entries.
        # ------------------------------------------------------------------
        clubs = [
            Club(
                name="AI & Robotics Lab Club",
                description=(
                    "Student-run club for projects in AI, robotics, and machine learning. "
                    "We do weekly hack nights and semester-long projects."
                ),
                tags="academic_stem_tech",
                meeting_time="Tue 18:00",
                location="Engineering Building Room 101",
            ),
            Club(
                name="Startup & Entrepreneurship Circle",
                description=(
                    "Discuss startup ideas, host pitch nights, and invite founders "
                    "and alumni to talk about building companies."
                ),
                tags="business_career,academic_stem_tech",
                meeting_time="Thu 19:00",
                location="Business School Lounge",
            ),
            Club(
                name="Campus Jazz Band",
                description=(
                    "Open jazz ensemble for all instruments and levels. "
                    "We rehearse weekly and perform once per semester."
                ),
                tags="creative_arts",
                meeting_time="Wed 19:30",
                location="Music Hall Studio 3",
            ),
            Club(
                name="Recreational Soccer Club",
                description=(
                    "Casual soccer games twice a week, open to all skill levels. "
                    "Great for staying active and meeting new people."
                ),
                tags="sports",
                meeting_time="Mon 17:00",
                location="Main Athletic Field",
            ),
            Club(
                name="Board Games & Tabletop Society",
                description=(
                    "Weekly board game nights with modern board games, card games, "
                    "and tabletop RPG one-shots."
                ),
                tags="gaming,creative_arts",
                meeting_time="Fri 19:00",
                location="Student Lounge",
            ),
            Club(
                name="Community Service Volunteers",
                description=(
                    "Organizes volunteering trips and service projects in the local community. "
                    "Transportation is usually provided."
                ),
                tags="service",
                meeting_time="Sat 10:00",
                location="Community Center",
            ),
            Club(
                name="Climate Action & Sustainability Group",
                description=(
                    "Student organization focused on climate activism, sustainability projects, "
                    "and campus-wide environmental campaigns."
                ),
                tags="activism_environment,service",
                meeting_time="Tue 17:30",
                location="Science Building Room 210",
            ),
            Club(
                name="Debate & Politics Forum",
                description=(
                    "Hosts weekly debates on current events and political issues, "
                    "plus practice sessions for competitions."
                ),
                tags="politics,academic_stem_tech",
                meeting_time="Thu 18:30",
                location="Humanities Building Room 305",
            ),
            Club(
                name="International & Cultural Exchange Club",
                description=(
                    "Cultural potlucks, language exchange, and events celebrating "
                    "different cultures on campus."
                ),
                tags="cultural",
                meeting_time="Fri 18:00",
                location="Global Lounge",
            ),
            Club(
                name="Interfaith Fellowship",
                description=(
                    "Discussion and community space for students from different faith "
                    "backgrounds. Weekly meetings and occasional retreats."
                ),
                tags="faith,service",
                meeting_time="Sun 16:00",
                location="Chapel Meeting Room",
            ),
        ]

        db.session.add_all(users + clubs)
        db.session.commit()

        print("Seed completed: inserted Users and Clubs with 10-tag vocab.")


if __name__ == "__main__":
    seed()
