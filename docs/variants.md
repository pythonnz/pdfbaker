# Document Variants

Document variants allow you to create multiple versions of the same document with
different content or settings. This is useful for:

- Creating different versions for different audiences
- Generating documents with different feature sets
- Producing localized versions
- Creating premium vs standard editions

## Basic Structure

Variants are defined in your document's `config.yaml`:

```yaml
filename: "My Document - {{ variant.name }}"

variants:
  - name: Standard
    pages:
      - cover
      - content
    content:
      features:
        - Basic Support
        - Standard SLA

  - name: Premium
    pages:
      - cover
      - content
      - premium_features
    content:
      features:
        - Premium Support
        - Priority SLA
        - Custom Integration
```

## Variant Configuration

Each variant can:

1. Define its own set of pages
2. Override document-level settings
3. Provide variant-specific content
4. Customize the processing workflow

### Page Selection

```yaml
variants:
  - name: Standard
    pages:
      - cover
      - content
  - name: Premium
    pages:
      - cover
      - content
      - premium_features
```

### Content Overrides

```yaml
variants:
  - name: Standard
    content:
      price: 100
      features:
        - Basic Support
  - name: Premium
    content:
      price: 200
      features:
        - Premium Support
        - Priority SLA
```

## Using Variants in Templates

Your SVG templates can access variant-specific content:

```xml
<svg>
  <text>Features for {{ variant.name }}:</text>
  {% for feature in variant.content.features %}
  <text>{{ feature }}</text>
  {% endfor %}
</svg>
```

## Best Practices

1. Use meaningful variant names that describe their purpose
2. Keep common content at the document level
3. Use YAML anchors for shared content between variants
4. Consider using variants for:
   - Different client tiers
   - Language/localization
   - Feature sets
   - Audience types
