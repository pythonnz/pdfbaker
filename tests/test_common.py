"""Tests for common functionality."""

import pytest

from pdfbaker.common import deep_merge, resolve_config


def test_deep_merge_basic():
    """Test basic dictionary merging."""
    base = {
        "title": "Document",
        "style": {
            "font": "Helvetica",
            "size": 12,
        },
    }
    update = {
        "title": "Updated Document",
        "style": {
            "size": 14,
        },
        "author": "John Doe",
    }
    expected = {
        "title": "Updated Document",
        "style": {
            "font": "Helvetica",
            "size": 14,
        },
        "author": "John Doe",
    }
    assert deep_merge(base, update) == expected


def test_deep_merge_nested():
    """Test merging of nested dictionaries."""
    base = {
        "document": {
            "title": "Main Document",
            "meta": {
                "author": "Jane Smith",
                "date": "2024-01-01",
            },
        },
        "style": {
            "font": "Arial",
            "colors": {
                "text": "black",
                "background": "white",
            },
        },
    }
    update = {
        "document": {
            "meta": {
                "date": "2024-04-01",
                "version": "1.0",
            },
        },
        "style": {
            "colors": {
                "text": "navy",
            },
        },
    }
    expected = {
        "document": {
            "title": "Main Document",
            "meta": {
                "author": "Jane Smith",
                "date": "2024-04-01",
                "version": "1.0",
            },
        },
        "style": {
            "font": "Arial",
            "colors": {
                "text": "navy",
                "background": "white",
            },
        },
    }
    assert deep_merge(base, update) == expected


def test_deep_merge_empty():
    """Test merging with empty dictionaries."""
    base = {
        "title": "Document",
        "style": {
            "font": "Helvetica",
        },
    }
    update = {}
    # Merging empty into non-empty should return non-empty
    assert deep_merge(base, update) == base
    # Merging non-empty into empty should return non-empty
    # pylint: disable=arguments-out-of-order
    assert deep_merge(update, base) == base


def test_resolve_config_basic():
    """Test basic template resolution."""
    config = {
        "name": "test",
        "title": "{{ name }} document",
    }
    expected = {
        "name": "test",
        "title": "test document",
    }
    assert resolve_config(config) == expected


def test_resolve_config_multiple_passes():
    """Test config that needs multiple passes to resolve."""
    config = {
        "name": "test",
        "title": "{{ name }} document",
        "filename": "{{ title }}.pdf",
    }
    expected = {
        "name": "test",
        "title": "test document",
        "filename": "test document.pdf",
    }
    assert resolve_config(config) == expected


def test_resolve_config_diamond_reference():
    """Test diamond-shaped reference pattern."""
    config = {
        "name": "test",
        "title": "{{ name }} document",
        "subtitle": "{{ name }} details",
        "header": "{{ title }} - {{ subtitle }}",
    }
    expected = {
        "name": "test",
        "title": "test document",
        "subtitle": "test details",
        "header": "test document - test details",
    }
    assert resolve_config(config) == expected


def test_resolve_config_circular():
    """Test circular reference handling."""
    config = {
        "a": "{{ b }}",
        "b": "{{ c }}",
        "c": "{{ a }}",
    }
    with pytest.raises(ValueError, match="Maximum number of iterations reached"):
        resolve_config(config)


def test_resolve_config_nested():
    """Test resolution in nested structures."""
    config = {
        "name": "test",
        "sections": [
            {"title": "{{ name }} section 1"},
            {"title": "{{ name }} section 2"},
        ],
        "meta": {
            "title": "{{ name }} document",
            "description": "About {{ meta.title }}",
        },
    }
    expected = {
        "name": "test",
        "sections": [
            {"title": "test section 1"},
            {"title": "test section 2"},
        ],
        "meta": {
            "title": "test document",
            "description": "About test document",
        },
    }
    assert resolve_config(config) == expected
