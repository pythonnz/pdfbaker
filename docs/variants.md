# Document Variants

Document variants allow you to create multiple versions of the same document with
different content or settings. This is useful for:

- Creating different versions for different audiences
- Generating documents with different feature sets
- Producing localized versions
- Creating standard vs premium editions

## Basic Structure

Variants are defined in your document's `config.yaml`:

```yaml
filename: "My Document - {{ variant.name }}"

variants:
  - name: Standard
    pages:
      - cover
      - content
    features:
      - Basic Support
      - Standard SLA

  - name: Premium
    pages:
      - cover
      - content
      - premium_features
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
    price: 100
    features:
      - Basic Support
  - name: Premium
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
  {% for feature in variant.features %}
  <text>{{ feature }}</text>
  {% endfor %}
</svg>
```

## Example

See [the variants example](../examples/variants) for a simple implementation of this in
action.
