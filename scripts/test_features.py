# scripts/test_features.py

from app import create_app
from app.extensions import db
from app.models import User, Club
from app.recommendation.features import build_feature_vector


def main():
    """Simple sanity check for build_feature_vector(user, club)."""
    app = create_app()

    with app.app_context():
        # Pick one user and one club from the database
        user = User.query.first()
        club = Club.query.first()

        if user is None or club is None:
            print("No User or Club found in the database. Did you run the seed script?")
            return

        # Build feature vector
        phi = build_feature_vector(user, club)

        print("=== Test: build_feature_vector ===")
        print(f"User: {user.id} / {user.email} / year={user.year} / interests={user.interests}")
        print(f"Club: {club.id} / {club.name} / tags={club.tags} / meeting_time={club.meeting_time}")
        print("----------------------------------")
        print("phi shape:", phi.shape)
        print("phi values:", phi.tolist())

        # Optional sanity check
        if phi.shape != (38,):
            print("WARNING: Expected feature vector of shape (38,), got:", phi.shape)
        else:
            print("OK: feature vector has shape (38,)")


if __name__ == "__main__":
    main()
