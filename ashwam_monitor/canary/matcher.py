from typing import List, Set, Tuple
from ..models.inputs import ParserItem, GoldItem


def normalize_span(span: str) -> str:
    """lowercase and strip for matching"""
    return span.lower().strip()


def items_match(parser_item: ParserItem, gold_item: GoldItem) -> bool:
    """
    check if parser item matches gold item
    matching on domain + evidence span + polarity
    """
    if parser_item.domain != gold_item.domain:
        return False

    if parser_item.polarity != gold_item.polarity:
        return False

    # evidence span matching - allow partial
    parser_span = normalize_span(parser_item.evidence_span)
    gold_span = normalize_span(gold_item.evidence_span)

    if parser_span == gold_span:
        return True

    # partial match - one contains the other
    if parser_span in gold_span or gold_span in parser_span:
        return True

    return False


def match_items(
    parser_items: List[ParserItem],
    gold_items: List[GoldItem]
) -> Tuple[int, int, int]:
    """
    match parser items against gold labels
    returns (matched, missed, extra)
    """
    matched = 0
    gold_matched: Set[int] = set()
    parser_matched: Set[int] = set()

    # find matches
    for pi, pitem in enumerate(parser_items):
        for gi, gitem in enumerate(gold_items):
            if gi in gold_matched:
                continue
            if items_match(pitem, gitem):
                matched += 1
                gold_matched.add(gi)
                parser_matched.add(pi)
                break

    missed = len(gold_items) - len(gold_matched)
    extra = len(parser_items) - len(parser_matched)

    return matched, missed, extra
