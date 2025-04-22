# Updated parser with narrowed scope for domestic grants only
from lxml import etree
from pathlib import Path
from typing import List
from pydantic import BaseModel

class Grant(BaseModel):
    recipient_name: str | None
    grant_amount: int | None
    grant_purpose: str | None
    # recipient_country: str | None
    # is_foreign: bool = False

def parse_990pf_file(xml_path: str) -> List[Grant]:
    tree = etree.parse(Path(xml_path))
    root = tree.getroot()

    ns = {'irs': root.nsmap.get(None)} if None in root.nsmap else {}

    grants = []

    POSSIBLE_GRANT_TAGS = [
        "GrantOrContributionPdDurYrGrp",
        "GrantOrContriPaidDuringYear"
    ]

    # collect all grant nodes under possible tags
    grant_nodes: List[etree._Element] = []
    for tag in POSSIBLE_GRANT_TAGS:
        found = root.findall(f".//irs:{tag}", namespaces=ns)
        if found:
            grant_nodes.extend(found)

    for node in grant_nodes:
        recipient_name = _find_text(node, ["RecipientBusinessName", "RecipientPersonNm"], ns)
        grant_amount = _find_int(node, ["GrantAmt", "Amt", "CashGrantAmt", "Amount"], ns)
        grant_purpose = _find_text(node, ["GrantOrContributionPurposeTxt", "GrantOrContributionPurpose"], ns)

        grants.append(Grant(
            recipient_name=recipient_name,
            grant_amount=grant_amount,
            grant_purpose=grant_purpose,
        ))

    return grants

def _find_text(parent, tags, ns):
    for tag in tags:
        parts = tag.split('/')
        node = parent
        for part in parts:
            found = node.find(f"irs:{part}", namespaces=ns)
            if found is None:
                node = None
                break
            node = found
        if node is not None and node.text:
            return node.text.strip()
    return None

def _find_int(parent, tags, ns):
    val = _find_text(parent, tags, ns)
    try:
        return int(val) if val else None
    except (ValueError, TypeError):
        return None


