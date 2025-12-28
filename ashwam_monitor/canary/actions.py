from ..models.enums import CanaryAction
from ..config import config


def determine_action(f1: float, evidence_rate: float) -> tuple:
    """
    decide what action to take based on canary metrics
    returns (action, reason)
    """
    thresholds = config.canary

    if f1 < thresholds.f1_rollback:
        return CanaryAction.ROLLBACK, f"f1 {f1:.2f} below rollback threshold {thresholds.f1_rollback}"

    if f1 < thresholds.f1_human_review:
        return CanaryAction.HUMAN_REVIEW, f"f1 {f1:.2f} below human review threshold {thresholds.f1_human_review}"

    if f1 < thresholds.f1_alert:
        return CanaryAction.ALERT, f"f1 {f1:.2f} below alert threshold {thresholds.f1_alert}"

    if evidence_rate < thresholds.min_evidence_match:
        return CanaryAction.ALERT, f"evidence match rate {evidence_rate:.2f} below threshold {thresholds.min_evidence_match}"

    return CanaryAction.PASS, "all metrics within acceptable range"
