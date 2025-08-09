---
id: MB.INSTRUCTIONS.v1
title: Instrukcje „Memory Bank” + Chain‑of‑Drafts + Uniwersalny Prompt
version: 1.0.0
status: approved
tags: [process, prompt, docs]
updated: 2025-08-08
owner: docs-owner
---

## Format wpisu (memory item)
Front‑matter (YAML) + treść Markdown. Pola: id, title, version (semver), tags, status (draft/approved/deprecated), author, createdAt, updatedAt, context, decision, rationale, impact {api, db, ui}, dependencies, links, successMetrics, todo, openQuestions, examples.

## Kategorie
- Vision/NFR, Architektura, Domain model, API contract, IA/UX, Content model, Data & SRS, DevEx, Security/Privacy, Roadmap & ADR.

## Procedura chain‑of‑drafts
1) Inicjalizacja: cel, użytkownik, ograniczenia, powiązania, źródła.
2) Draft A (30–40%): szkic pól, ryzyka, minimalne API/DB.
3) Krytyka A: braki, sprzeczności, pytania kontrolne.
4) Draft B (70–85%): doprecyzowanie pól, przykłady, edge cases.
5) Pojednanie + checklista akceptacji: zgodność z Vision/NFR/API/DB/UX.
6) Finalizacja: wersja, changelog, status.
7) Dyfuzja: PR‑y, migracje, aktualizacja OpenAPI/IA.

## Uniwersalny prompt (wklej do narzędzia AI)
Rola: „Jesteś architektem i technical writerem dla projektu ITF Taekwon‑Do Handbook. Tworzysz wpisy memory banku zgodnie z formatem i chain‑of‑drafts. Dbaj o spójność z NFR (offline‑first, multimedia, PL/EN/KR).”

Wejście użytkownika:
- Temat wpisu:
- Cel biznesowy/UX:
- Zakres (in/out):
- Ograniczenia (technologia, wydajność, bezpieczeństwo):
- Powiązania (inne wpisy/komponenty):
- Źródła/referencje:

Instrukcje wykonania:
1) Wygeneruj Draft A (streszczenie + ryzyka + minimalne pola danych/API).
2) Wygeneruj Krytykę A (braki, pytania, alternatywy).
3) Wygeneruj Draft B (pełne pola, przykłady, schemat API/DB, przypadki brzegowe).
4) Wygeneruj Pojednanie + Checklistę akceptacji (10 punktów).
5) Wygeneruj Final (front‑matter + treść: kontekst, decyzje, wpływ, linki, testy akceptacyjne).

Zasady:
- Konkret; przykłady wykonalne w Django/Flutter.
- Oznacz decyzje nieodwracalne i koszt zmiany.
- Dodaj testy akceptacyjne (API, UI, dane).
- Linkuj do źródeł (Medium/GitHub/YouTube) tam gdzie sensowne.

## Przykład minimalnego JSON (dla generatorów)
```json
{
  "id": "ENT.TECHNIQUE.v1",
  "title": "Model i API: Technique",
  "version": "1.0.0",
  "tags": ["entity", "api", "content"],
  "status": "approved",
  "context": "Leksykon technik z multimediami i i18n",
  "decision": "DRF REST, OpenAPI, media via S3 signed URLs, versioned content",
  "impact": {"db": ["Technique", "MediaAsset"], "api": ["/api/techniques"], "ui": ["Leksykon > Karta"]},
  "links": ["https://github.com/pygraz/django-flutter-example"],
  "openQuestions": [],
  "examples": {
    "GET": "/api/techniques?category=kick&belt=7",
    "ResponseItem": {"id":1,"names":{"pl":"Ap Chagi","en":"Front Kick","kr":"앞차기"},"videos":{"demo":"..."}}
  }
}
```

