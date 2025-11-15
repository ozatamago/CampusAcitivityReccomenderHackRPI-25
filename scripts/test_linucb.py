# scripts/test_linucb.py

from app import create_app
from app.extensions import db
from app.models import User, Club
from app.recommendation.linucb import GLOBAL_LINUCB


def simulate_reward(user, club) -> float:
    """
    Simple fake reward function for testing.

    For now:
      reward = 1.0 if user and club share at least one tag,
      otherwise 0.0.
    This is just for sanity check and not used in production.
    """
    from app.recommendation.utils import parse_tags

    user_tags = parse_tags(getattr(user, "interests", ""))
    club_tags = parse_tags(getattr(club, "tags", ""))

    overlap = user_tags & club_tags
    return 1.0 if len(overlap) > 0 else 0.0


def main():
    """Simple test loop for the global LinUCB agent."""
    app = create_app()

    with app.app_context():
        users = User.query.all()
        clubs = Club.query.all()

        if not users or not clubs:
            print("No users or clubs in the database. Did you run the seed script?")
            return

        user = users[0]
        print(f"Testing LinUCB with user: {user.id} / {user.email} / interests={user.interests}")

        # Use a small set of candidate clubs (e.g. first 5)
        candidate_clubs = clubs[:5]
        print("Candidate clubs:")
        for c in candidate_clubs:
            print(f"- {c.id}: {c.name} (tags={c.tags})")

        # Reset global LinUCB state
        GLOBAL_LINUCB.reset()

        # Run a few rounds of (select -> simulate reward -> update)
        num_rounds = 100
        print("\n=== LinUCB test loop ===")
        for t in range(1, num_rounds + 1):
            best_club, score = GLOBAL_LINUCB.select_best(user, candidate_clubs)
            if best_club is None:
                print("No best club found.")
                break

            # Simulate reward based on tag overlap
            reward = simulate_reward(user, best_club)
            GLOBAL_LINUCB.update(user, best_club, reward)

            print(
                f"Round {t:2d}: selected club {best_club.id} / {best_club.name}, "
                f"score={score:.4f}, reward={reward}"
            )

        print("\nTest finished.")


if __name__ == "__main__":
    main()
