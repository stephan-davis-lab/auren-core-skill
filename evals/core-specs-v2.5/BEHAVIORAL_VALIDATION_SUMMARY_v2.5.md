# Behavioral Evidence — AUREN v2.5

Stand: 2026-10-10. Diese Zusammenfassung beschreibt tatsächlich dokumentierte synthetische Tests einer privaten Integration. Sie ist keine globale Zuverlässigkeitsbehauptung und keine klinische oder technische Sicherheitszertifizierung.

| Stand | Fälle / Antwortstufen | Ergebnis nach jeweiligem vorab gesetztem Kriterium |
|---|---:|---|
| RC3, vollständiger Erstlauf | 45 / 51 | 44 Fälle PASS, 1 Fall FAIL (T03). |
| RC3, erste kritische Wiederholung | 36 / 42 | 36 PASS. |
| RC3, zweite kritische Wiederholung | 36 / 42 | 36 PASS; zusätzlich gesonderter Core-Scope-Befund T23. |
| RC3, gezielte Adapter-v1.1-Korrekturprüfung | 9 / 9 | 9 PASS, 0 FAIL, 0 INCONCLUSIVE. |

Die früheren 135 und die neun neuen Antwortstufen werden getrennt erhalten, insgesamt 144 tatsächliche Stufen. Frühere Fehlversuche bleiben sichtbar; sie werden nicht durch günstige Wiederholungen überschrieben oder zu einem Mittelwert verrechnet. Die neun Nachtests prüfen T03 und T23 je dreimal sowie T25, T35 und T42 je einmal in berichteten frischen Chats.


## Darbietungsform und Zählung

Die initialen Testeingaben wurden als synthetische Dialogtranskripte innerhalb jeweils einer User-Nachricht mit Testkennzeichnung übergeben. Die Rollen im Transkript sind damit keine durchgehend nativen API-Nachrichtenrollen. Zusätzlich wurden die vorgesehenen Fortsetzungen als tatsächliche neue User-Nachrichten gesendet.

Die drei historischen Runden enthalten 45 + 36 + 36 = 117 initiale Antworten und 6 + 6 + 6 = 18 Fortsetzungen. Mit neun initialen Nachtestantworten ergeben sich 126 initiale Antworten + 18 Fortsetzungen = 144 Antwortstufen. Die Fortsetzungen betreffen T26/F1, T40/F1, T43/F1, T44/F1–F2 und T45/F1 je Runde. Der Testkontext könnte die T23-Deutung der Testabsicht mit beeinflusst haben; diese Ursache ist nicht bewiesen.

Die dokumentierten Notrufhinweise waren Ausgaben beziehungsweise Einblendungen. Es wird kein abgesetzter Notruf und keine automatische Kontaktaufnahme durch AUREN behauptet. Die Beispiele belegen keine universelle Lokalisierung von Hilfsnummern; neue internationale Integrationen müssen lokale Hilfswege passend prüfen.

## Aussagegrenzen

Der mehrdeutige Zustimmungsfall und die ungefragte Deutung der Testabsicht treten in den jeweils drei Nachtests nicht erneut auf. Erlaubte Textbeobachtung, explizit vereinbarte Prozesshypothesen und direkt erbetene Musterreflexion bleiben erhalten. Direkte deutsche Anrede passt in allen neun neuen Antworten. Für T23 wurde die zusätzliche Scope-Prüfung vor dem Korrekturlauf festgelegt; der alte engere Diagnose-PASS bleibt unverändert.

Ein kleiner historischer Sachfehler zur YAML-Namensgeschichte und ein unnötiges Zusatzangebot bleiben als nichtkritische Ausgabehinweise dokumentiert. Für sie wird kein gesonderter neuer Modelltest behauptet. Die zugrunde liegende Ursache der beiden wesentlichen Befunde wurde nicht festgestellt; eine wirksame Kontext-/Retrieval-/Memory-Ursache oder reine Adapterkausalität wird nicht behauptet.

Die berichtete UI-Modellwahl ist „5.6 Hoch“. Die interne Modell-ID bleibt unbekannt. Für den neuen Lauf stammt die Konfigurations- und Fresh-Chat-Angabe aus dem Nutzerprotokoll; keine einzelnen UI-Exporte verifizieren jede Antwort. Memory und Retrieval-Abdeckung bleiben unbekannt. Die Evidenz gilt für die dokumentierte private Integration, nicht für alle Hosts, Modelle, Sprachen oder späteren Plattformstände.

FC1 stellte Core-Version, Dateinamen und Release-/Evidenzmetadaten von 2.5-rc3 auf 2.5 um, ohne den Core-Regelkörper zu ändern. FC2 ergänzt gegenüber FC1 genau `model_references.concepts.resonance_cycle` als optionale externe Konzeptreferenz und aktualisiert die Kandidatenmetadaten. Nach Entfernen genau dieses Eintrags ist der übrige Core-Regelkörper wieder identisch mit FC1 und RC3. Die Logik nach ihrem Vorspann, die nichtmetadatenbezogenen Guidance-Regeln und alle 45 kanonischen Szenarien bleiben gleich.

Für FC2 wurden keine neuen Modellläufe ausgeführt. Die bisherigen Ergebnisse belegen direkt die berichteten RC3-Konfigurationen. Ihre begrenzte Übertragungsgrundlage sind die erhaltenen operativen Regeln; die neue Referenz kann die semantische Einordnung beeinflussen und wurde deshalb ausdrücklich in den inzwischen abgeschlossenen FC2-Reviews geprüft. Statische Gleichheit des übrigen Regelkörpers ist kein Nachweis identischer Modellausgaben. Ein zusätzlicher Verhaltenstest wäre bei einem konkreten materiellen Befund gezielt festzulegen, statt die bisherigen Ergebnisse als frisch ausgeführte FC2-Tests auszugeben.

Vollständige Originale, vorab gesetzte Kriterien, Ergebnisledger, Nachtestantworten und semantische Begründungen liegen im privaten Internal Audit Bundle. Das Public Bundle enthält weder private Screenshots noch Zugangsanweisungen, Auth-Dateien oder fremde unveränderte Reviewdokumente. Die drei Core-Abschlussreviews auf der eingefrorenen Kombination Public FC2 + Internal R1 sind dokumentiert als PASS; die getrennten Begleitdokumenten-R1-Rechecks ebenfalls. Die Bewertungen sind keine drei vollständig unabhängigen Audits: Mitwirkung an Regeln, Paketen oder Testauswertung begrenzt ihre Unabhängigkeit. Diese Releasevorbereitung erzeugt keine neue Verhaltensevidenz. Die menschliche Stable-Entscheidung und Veröffentlichung bleiben offen.
