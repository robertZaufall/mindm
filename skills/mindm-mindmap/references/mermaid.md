# Mermaid metadata guide

Use this when constructing **full Mermaid** input for `create-from-mermaid`.
Simplified Mermaid (indent-only) does not use metadata comments.

## Rules

- Every line must be valid Mermaid and include a topic label, e.g. `[Topic]`.
- Root topic is just a label, e.g. `[Central Topic]`.
- Full syntax attaches JSON metadata after `%%` on the same line.

## Metadata example

```
mindmap
  [Topic] %% {"id": 1, "notes": {"text": "Notes"}, "links": [{"text": "label", "url": "https://example.com"}], "references": [{"id_1": 1, "id_2": 2, "direction": 1}], "image": {"text": "C:\\path\\to\\image.png"}, "icons": [{"text": "StockIcon-36", "is_stock_icon": true, "index": 36}], "tags": ["tag1"]}
```

## Icon metadata (Windows stock icons)

Use:

```
"icons": [{"text": "StockIcon-<index>", "is_stock_icon": true, "index": <index>}]
```

Available stock icon indices:

- Arrow Down(66), Arrow Left(65), Arrow Right(37), Arrow Up(36)
- Bomb(51), Book(67), Broken Connection(69), Calendar(8), Camera(41)
- Cellphone(40), Check(62), Clock(7), Coffee Cup(59), Dollar(15)
- Email(10), Emergency(49), Euro(16), Exclamation Mark(44), Fax(42)
- Flag Black(20), Flag Blue(18), Flag Green(19), Flag Orange(21), Flag Purple(23)
- Flag Red(17), Flag Yellow(22), Folder(71), Glasses(53), Hourglass(48)
- House(13), Information(70), Judge Hammer(54), Key(52), Letter(9)
- Lightbulb(58), Magnifying Glass(68), Mailbox(11)
- Marker 1(25), Marker 2(26), Marker 3(27), Marker 4(28)
- Marker 5(29), Marker 6(30), Marker 7(31), Meeting(61), Megaphone(12)
- No Entry(50), Note(63), On Hold(47)
- Padlock Locked(34), Padlock Unlocked(35), Phone(39), Question Mark(45)
- Redo(57), Resource 1(32), Resource 2(33), Rocket(55), Rolodex(14)
- Scales(56), Smiley Angry(5), Smiley Happy(2), Smiley Neutral(3), Smiley Sad(4)
- Smiley Screaming(6), Stop(43), Thumbs Down(64), Thumbs Up(46)
- Traffic Lights Red(24), Two End Arrow(38), Two Feet(60)
