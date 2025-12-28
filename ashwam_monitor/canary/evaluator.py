from typing import List, Tuple
from ..models.inputs import ParserItem, GoldItem


def compute_precision_recall_f1(matched: int, missed: int, extra: int) -> Tuple[float, float, float]:
    """
    standard p r f1 calculation
    """
    total_predicted = matched + extra
    total_actual = matched + missed

    precision = matched / total_predicted if total_predicted > 0 else 0.0
    recall = matched / total_actual if total_actual > 0 else 0.0

    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0

    return precision, recall, f1


def compute_evidence_match_rate(
    parser_items: List[ParserItem],
    gold_items: List[GoldItem]
) -> float:
    """
    how many parser items have evidence that matches gold
    this is about span grounding not just count
    """
    if not parser_items or not gold_items:
        return 0.0

    matched = 0
    for pitem in parser_items:
        p_span = pitem.evidence_span.lower().strip()
        for gitem in gold_items:
            g_span = gitem.evidence_span.lower().strip()
            if p_span == g_span or p_span in g_span or g_span in p_span:
                matched += 1
                break

    return matched / len(parser_items)
