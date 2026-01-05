"""
Unit tests for ANAFI advanced analysis tools.

Run with: pytest tests/test_advanced_analysis.py -v
"""
import pytest
from src.models.financial_data import BusinessInputData
from src.tools.advanced_analysis_tools import (
    project_cashflow,
    generate_income_statement,
    create_business_canvas
)


@pytest.fixture
def sample_business_data():
    """Sample business data for testing."""
    return {
        "nombre_negocio": "Test Restaurant",
        "tipo_negocio": "restaurante",
        "costos_fijos_mensuales": 5000.0,
        "costo_variable_unitario": 3.0,
        "precio_venta_unitario": 10.0,
        "volumen_ventas_estimado": 1000,
        "inversion_inicial": 50000.0
    }


@pytest.fixture
def mock_state(sample_business_data):
    """Mock state with sample business data."""
    return {
        "files": {
            "/business_data/input_data.json": {
                "data": sample_business_data,
                "content": str(sample_business_data)
            }
        }
    }


class TestProjectCashflow:
    """Tests for cashflow projection."""
    
    def test_cashflow_12_months(self, mock_state):
        """Test 12-month cashflow projection."""
        result = project_cashflow(12, mock_state, "test_id")
        
        assert "12 meses" in result
        assert "Flujo mensual" in result
        assert "✅" in result
    
    def test_cashflow_custom_months(self, mock_state):
        """Test custom month projection."""
        result = project_cashflow(6, mock_state, "test_id")
        
        assert "6 meses" in result
    
    def test_cashflow_max_months(self, mock_state):
        """Test maximum months limit."""
        result = project_cashflow(30, mock_state, "test_id")
        
        assert "Error" in result or "❌" in result
    
    def test_cashflow_negative_flow(self, mock_state):
        """Test cashflow with negative flow."""
        # Create scenario with losses
        mock_state["files"]["/business_data/input_data.json"]["data"]["costos_fijos_mensuales"] = 15000.0
        
        result = project_cashflow(12, mock_state, "test_id")
        
        assert "ALERTA" in result or "⚠️" in result
    
    def test_cashflow_saves_to_state(self, mock_state):
        """Test that cashflow is saved to state."""
        project_cashflow(12, mock_state, "test_id")
        
        assert "/analysis/cashflow_projection.json" in mock_state.get("files", {})


class TestGenerateIncomeStatement:
    """Tests for income statement generation."""
    
    def test_income_statement_structure(self, mock_state):
        """Test income statement structure."""
        result = generate_income_statement(mock_state, "test_id")
        
        assert "Ventas Totales" in result
        assert "Costos Variables" in result
        assert "Utilidad Bruta" in result
        assert "Costos Fijos" in result
        assert "Utilidad Neta" in result
        assert "✅" in result
    
    def test_income_statement_margins(self, mock_state):
        """Test that margins are calculated."""
        result = generate_income_statement(mock_state, "test_id")
        
        assert "Margen Bruto" in result
        assert "Margen Neto" in result
        assert "%" in result
    
    def test_income_statement_saves_to_state(self, mock_state):
        """Test that income statement is saved."""
        generate_income_statement(mock_state, "test_id")
        
        assert "/analysis/income_statement.json" in mock_state.get("files", {})


class TestCreateBusinessCanvas:
    """Tests for Business Model Canvas creation."""
    
    def test_canvas_creation(self, mock_state):
        """Test canvas creation."""
        result = create_business_canvas(mock_state, "test_id")
        
        assert "Business Model Canvas" in result
        assert "Test Restaurant" in result
        assert "✅" in result
    
    def test_canvas_includes_metrics(self, mock_state):
        """Test that canvas includes financial metrics."""
        result = create_business_canvas(mock_state, "test_id")
        
        assert "Fuentes de Ingresos" in result or "$" in result
        assert "Estructura de Costos" in result or "Costos" in result
    
    def test_canvas_saves_to_state(self, mock_state):
        """Test that canvas is saved."""
        create_business_canvas(mock_state, "test_id")
        
        assert "/analysis/business_canvas.json" in mock_state.get("files", {})


class TestAdvancedAnalysisIntegration:
    """Integration tests for advanced analysis tools."""
    
    def test_all_tools_work_together(self, mock_state):
        """Test that all advanced analysis tools work together."""
        # Run all tools
        cashflow_result = project_cashflow(12, mock_state, "test_id")
        income_result = generate_income_statement(mock_state, "test_id")
        canvas_result = create_business_canvas(mock_state, "test_id")
        
        # All should succeed
        assert "✅" in cashflow_result
        assert "✅" in income_result
        assert "✅" in canvas_result
        
        # All should save to state
        assert "/analysis/cashflow_projection.json" in mock_state["files"]
        assert "/analysis/income_statement.json" in mock_state["files"]
        assert "/analysis/business_canvas.json" in mock_state["files"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
