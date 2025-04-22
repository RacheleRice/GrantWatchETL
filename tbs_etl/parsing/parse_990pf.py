from lxml import etree
from pathlib import Path
from typing import List
from pydantic import BaseModel

class Grant(BaseModel):
    recipient_name: str | None
    grant_amount: int | None
    grant_purpose: str | None
    recipient_country: str | None
    is_foreign: bool = False

def parse_990pf_file(xml_path: str) -> List[Grant]:
    tree = etree.parse(Path(xml_path))
    root = tree.getroot()

    ns = {'irs': root.nsmap.get(None)} if None in root.nsmap else {}

    grants = []

    grant_nodes = root.findall(".//irs:GrantOrContributionPdDurYrGrp", namespaces=ns)
    if not grant_nodes:
        grant_nodes = root.findall(".//irs:GrantOrContriPaidDuringYear", namespaces=ns)

    for node in grant_nodes:
        recipient_name = _find_text(node, ["RecipientBusinessName", "RecipientPersonNm"], ns)
        grant_amount = _find_int(node, ["Amt", "Amount"], ns)
        grant_purpose = _find_text(node, ["GrantOrContributionPurposeTxt", "GrantOrContributionPurpose"], ns)
        country = _find_text(node, ["RecipientForeignAddress/ForeignCountryCd"], ns)
        is_foreign = country is not None

        grants.append(Grant(
            recipient_name=recipient_name,
            grant_amount=grant_amount,
            grant_purpose=grant_purpose,
            recipient_country=country,
            is_foreign=is_foreign
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
    except ValueError:
        return None
