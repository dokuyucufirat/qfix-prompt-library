# QFIX Prompt Library

Direct prompt editing repository for Voice AI system prompts.

## Structure

```
prompts/
├── protel/           # Protel (Hotel Management)
│   ├── inbound/      # Support calls
│   └── outbound/     # Surveys
├── narpos/           # NarPOS (POS Systems)
│   ├── inbound/      # Technical support
│   └── outbound/     # Surveys & Sales
└── altintay/         # Altintay (Customer Service)
    └── outbound/     # Welcome & Surveys
```

## File Format

Each product has a single `system_prompt.txt` file containing the complete Voice AI prompt.

```
prompts/{client}/{call_type}/{product}/
├── system_prompt.txt    # Active prompt
└── .versions/           # Version history
```

## Placeholders

Prompts use `{placeholder_name}` syntax for dynamic content:
- `{customer_name}` - Customer's name
- `{product_name}` - Product name
- `{company_name}` - Company name

## Editing

This repository is managed by the **Creative Support Team** in QFIX AI Crew.
Direct edits are made via Aider without build scripts.

## Version History

Each edit creates a version backup in `.versions/` folder with timestamp.

