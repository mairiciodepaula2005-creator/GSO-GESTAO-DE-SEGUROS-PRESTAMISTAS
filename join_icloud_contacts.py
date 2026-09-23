import json
import re
import sys
import unicodedata
from collections import defaultdict
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from pypdf import PdfReader

PDF_PATH = r"C:\Users\Samsung\Downloads\Contatos do iCloud.pdf"
FIREBASE_URL = "https://gsp---gerenciador-de-seg-default-rtdb.firebaseio.com/gsp/clients.json"


def normalize(value):
    text = unicodedata.normalize("NFD", str(value or ""))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", text.lower()).strip()


def phone_digits(value):
    digits = re.sub(r"\D", "", str(value or ""))
    if len(digits) == 10 or len(digits) == 11:
        return "55" + digits
    return digits


def missing_phone(client):
    return len(phone_digits(client.get("number"))) < 12


def extract_contacts():
    contacts = []
    reader = PdfReader(PDF_PATH)
    pattern = re.compile(
        r"(?ms)(?:^|\n)(.+?)(?:\s+)(?:Celular|Telefone)\s*([+\d][\d\s()\-]{7,})"
    )
    for page in reader.pages:
        text = page.extract_text() or ""
        text = re.sub(r"\n?23/09/2026,[^\n]*\nhttps://www\.icloud\.com/contacts/\s*\d+/\d+", "", text)
        text = text.replace("nome endereço e-mail telefone\n", "")
        for raw_name, raw_phone in pattern.findall(text):
            name = re.sub(r"\s+", " ", raw_name).strip()
            phone = phone_digits(raw_phone)
            if len(name) >= 3 and len(phone) >= 12:
                contacts.append((name, phone))
    return contacts


def contact_matches(client_name, contacts):
    client_norm = normalize(client_name)
    client_tokens = set(client_norm.split())
    if len(client_tokens) < 2:
        return []
    exact = [(name, phone) for name, phone in contacts if normalize(name) == client_norm]
    if exact:
        return exact

    candidates = []
    for name, phone in contacts:
        contact_norm = normalize(name)
        contact_tokens = set(contact_norm.split())
        common = client_tokens & contact_tokens
        # Requires every client name token to be present in the contact name.
        # This safely accepts contacts with helpful extra labels like "Integra".
        if client_tokens <= contact_tokens and len(common) >= 2:
            candidates.append((name, phone))
    return candidates


def main():
    with urlopen(FIREBASE_URL, timeout=30) as response:
        raw = json.load(response)
    is_list = isinstance(raw, list)
    pairs = list(enumerate(raw)) if is_list else list(raw.items())
    contacts = extract_contacts()
    updated = 0
    ambiguous = 0
    unmatched = 0

    for key, client in pairs:
        if not isinstance(client, dict) or not missing_phone(client):
            continue
        matches = contact_matches(client.get("name"), contacts)
        unique_phones = {phone for _, phone in matches}
        if len(unique_phones) == 1:
            client["number"] = next(iter(unique_phones))
            updated += 1
        elif len(unique_phones) > 1:
            ambiguous += 1
        else:
            unmatched += 1

    summary = {
        "contacts_extracted": len(contacts),
        "clients_checked_without_phone": updated + ambiguous + unmatched,
        "safe_matches_to_update": updated,
        "ambiguous_skipped": ambiguous,
        "not_found": unmatched
    }
    print(json.dumps(summary, ensure_ascii=False))

    with open("phone_join_preview.json", "w", encoding="utf-8") as stream:
        json.dump(raw, stream, ensure_ascii=False)
    with open("phone_join_summary.json", "w", encoding="utf-8") as stream:
        json.dump(summary, stream, ensure_ascii=False)

def apply_targeted_updates():
    with urlopen(Request(FIREBASE_URL, headers={"X-Firebase-ETag": "true"}), timeout=30) as response:
        current = json.load(response)
        etag = response.headers.get("ETag")
    with open("phone_join_preview.json", encoding="utf-8") as stream:
        preview = json.load(stream)

    updates = {}
    if isinstance(current, list) and isinstance(preview, list):
        for index, (old, proposed) in enumerate(zip(current, preview)):
            if isinstance(old, dict) and isinstance(proposed, dict) and missing_phone(old) and not missing_phone(proposed):
                updates[f"{index}/number"] = proposed["number"]
    elif isinstance(current, dict) and isinstance(preview, dict):
        for key, old in current.items():
            proposed = preview.get(key)
            if isinstance(old, dict) and isinstance(proposed, dict) and missing_phone(old) and not missing_phone(proposed):
                updates[f"{key}/number"] = proposed["number"]
    else:
        raise RuntimeError("A estrutura atual da base não corresponde à prévia validada.")

    if not updates:
        print("Nenhum telefone pendente para atualizar.")
        return
    request = Request(
        FIREBASE_URL,
        data=json.dumps(updates, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PATCH",
    )
    try:
        with urlopen(request, timeout=60):
            pass
    except HTTPError as error:
        raise RuntimeError(f"Firebase recusou a atualização: {error.code} {error.read().decode('utf-8', 'replace')}")
    print(json.dumps({"targeted_phone_updates": len(updates)}, ensure_ascii=False))

def verify_targeted_updates():
    with urlopen(FIREBASE_URL, timeout=30) as response:
        current = json.load(response)
    with open("phone_join_preview.json", encoding="utf-8") as stream:
        preview = json.load(stream)
    current_values = current if isinstance(current, list) else list(current.values())
    preview_values = preview if isinstance(preview, list) else list(preview.values())
    expected = confirmed = 0
    for old, proposed in zip(current_values, preview_values):
        if not isinstance(old, dict) or not isinstance(proposed, dict):
            continue
        proposed_number = phone_digits(proposed.get("number"))
        if proposed_number and len(proposed_number) >= 12 and old.get("name") == proposed.get("name"):
            # Counts only contacts that were newly suggested by this join.
            if old.get("number") == proposed.get("number"):
                confirmed += 1
    print(json.dumps({"records_with_preview_phone_confirmed": confirmed}, ensure_ascii=False))


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply_targeted_updates()
    elif "--verify" in sys.argv:
        verify_targeted_updates()
    else:
        main()
