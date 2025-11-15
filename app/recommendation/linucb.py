# app/recommendation/linucb.py
from __future__ import annotations

from typing import List, Tuple, Optional
import numpy as np

from app.recommendation.features import build_feature_vector


class LinUCB:
    """
    Simple global LinUCB agent.

    We use a shared linear model for all users and clubs:
      r_t = phi_t^T theta + noise
    where phi_t is the 38-dim feature vector built from (user, club).

    A and b are updated online:
      A <- A + phi phi^T
      b <- b + r phi

    For recommendation, we compute:
      mean = phi^T theta_hat
      var  = sqrt(phi^T A^{-1} phi)
      ucb  = mean + alpha * var
    and choose the club with the highest ucb.
    """

    def __init__(self, dim: int, alpha: float = 1.0, lambda_reg: float = 1.0) -> None:
        self.dim = dim
        self.alpha = alpha
        self.lambda_reg = lambda_reg

        # A is the design matrix (d x d), initialized as lambda * I
        self.A = lambda_reg * np.eye(dim, dtype=float)
        # b is the response vector (d)
        self.b = np.zeros(dim, dtype=float)

    def reset(self) -> None:
        """Reset A and b to the initial state."""
        self.A = self.lambda_reg * np.eye(self.dim, dtype=float)
        self.b = np.zeros(self.dim, dtype=float)

    def _theta_hat(self) -> np.ndarray:
        """Compute theta_hat = A^{-1} b using a linear solver."""
        return np.linalg.solve(self.A, self.b)

    def _ucb_score(self, phi: np.ndarray) -> float:
        """
        Compute the LinUCB score for a single feature vector phi.

        score = phi^T theta_hat + alpha * sqrt(phi^T A^{-1} phi)
        """
        # Estimate theta
        theta_hat = self._theta_hat()

        # Predicted mean reward
        mean = float(phi @ theta_hat)

        # Compute A^{-1} phi using a linear solver (avoid explicit inverse)
        A_inv_phi = np.linalg.solve(self.A, phi)
        var = float(np.sqrt(phi @ A_inv_phi))

        return mean + self.alpha * var

    def select_best(
        self,
        user,
        candidate_clubs: List,
    ) -> Tuple[Optional[object], Optional[float]]:
        """
        Select the best club for the given user from the candidate list
        according to the LinUCB score.

        Returns:
            (best_club, best_score) or (None, None) if no candidates.
        """
        if not candidate_clubs:
            return None, None

        best_club = None
        best_score = None

        for club in candidate_clubs:
            phi = build_feature_vector(user, club)
            score = self._ucb_score(phi)

            if best_score is None or score > best_score:
                best_score = score
                best_club = club

        return best_club, best_score

    def rank(
        self,
        user,
        candidate_clubs: List,
        top_k: int = 5,
    ) -> List[Tuple[object, float]]:
        """
        Rank candidate clubs for the given user by LinUCB score.

        Returns:
            A list of (club, score) sorted by score in descending order.
        """
        scored = []
        for club in candidate_clubs:
            phi = build_feature_vector(user, club)
            score = self._ucb_score(phi)
            scored.append((club, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def update(self, user, club, reward: float) -> None:
        """
        Update A and b using the observed reward for (user, club).

        Args:
            reward: observed reward, e.g. 1.0 for like, 0.0 for dislike.
        """
        phi = build_feature_vector(user, club)
        # A <- A + phi phi^T
        self.A += np.outer(phi, phi)
        # b <- b + r phi
        self.b += reward * phi

GLOBAL_LINUCB = LinUCB(dim=38, alpha=1.0, lambda_reg=1.0)
