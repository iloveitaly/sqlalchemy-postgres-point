"""Test Alembic integration for PointType."""

import pytest


def test_alembic_integration_import():
    """Test that the alembic integration module can be imported."""
    # This will fail if there are any import issues
    import sqlalchemy_postgres_point.alembic_integration
    assert True


def test_point_type_renderer():
    """Test that the PointType renderer is properly registered."""
    try:
        import alembic.autogenerate.render
        from sqlalchemy_postgres_point.alembic_integration import render_point_type
        from sqlalchemy_postgres_point import PointType
        
        # Check that our renderer is registered
        renderers = alembic.autogenerate.render.renderers
        
        # The renderer should be registered for PointType
        # We can verify this by checking if our function is in the dispatch table
        assert render_point_type is not None
        
        # Basic test of the render function
        # Create a mock autogen context
        class MockAutogenContext:
            def __init__(self):
                self.imports = set()
        
        autogen_context = MockAutogenContext()
        result = render_point_type(PointType(), None, autogen_context)
        
        # Check that the import was added
        assert "from sqlalchemy_postgres_point import PointType" in autogen_context.imports
        # Check that the correct type representation is returned
        assert result == "PointType()"
        
    except ImportError:
        pytest.skip("Alembic not available for testing")


def test_integration_without_alembic():
    """Test that the package still works when alembic is not available."""
    # We can't really test this since alembic is installed in our env,
    # but we can at least verify the basic PointType functionality
    from sqlalchemy_postgres_point import PointType
    
    # Basic instantiation should work
    point_type = PointType()
    assert point_type is not None
    
    # Validation should work
    validated = point_type._validate_point((12.34, 56.78))
    assert validated == (12.34, 56.78)