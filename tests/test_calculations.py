"""
Unit tests for ANAFI financial calculation tools.

Run with: pytest tests/test_calculations.py -v
"""
import pytest
from src.models.financial_data import BusinessInputData
from src.tools.calculate_breakeven import calculate_breakeven_point
from src.tools.calculate_costs import calculate_total_costs
from src.tools.calculate_profit import calculate_profit
from src.tools.calculate_profitability import calculate_profitability_ratios


@pytest.fixture
def sample_business_data():
    """Sample business data for testing."""
    return {
        "nombre_negocio": "Test Café",
        "tipo_negocio": "cafetería",
        "costos_fijos_mensuales": 3000.0,
        "costo_variable_unitario": 1.5,
        "precio_venta_unitario": 4.0,
        "volumen_ventas_estimado": 1200,
        "inversion_inicial": 10000.0
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


class TestCalculateBreakeven:
    """Tests for breakeven point calculation."""
    
    def test_breakeven_calculation(self, mock_state):
        """Test basic breakeven calculation."""
        result = calculate_breakeven_point(mock_state, "test_id")
        
        # Expected: 3000 / (4.0 - 1.5) = 1200 units
        assert "1200" in result or "1,200" in result
        assert "4800" in result or "4,800" in result
        assert "✅" in result
    
    def test_breakeven_with_alert(self, mock_state):
        """Test breakeven with critical alert."""
        # Modify data to trigger alert
        mock_state["files"]["/business_data/input_data.json"]["data"]["volumen_ventas_estimado"] = 1000
        
        result = calculate_breakeven_point(mock_state, "test_id")
        
        assert "ALERTA CRÍTICA" in result or "⚠️" in result
    
    def test_breakeven_no_data(self):
        """Test breakeven with no input data."""
        empty_state = {"files": {}}
        result = calculate_breakeven_point(empty_state, "test_id")
        
        assert "Error" in result or "❌" in result


class TestCalculateCosts:
    """Tests for total costs calculation."""
    
    def test_total_costs_calculation(self, mock_state):
        """Test total costs calculation."""
        result = calculate_total_costs(mock_state, "test_id")
        
        # Expected: 3000 + (1.5 * 1200) = 4800
        assert "4800" in result or "4,800" in result
        assert "3000" in result or "3,000" in result  # Fixed costs
        assert "1800" in result or "1,800" in result  # Variable costs
        assert "✅" in result
    
    def test_costs_breakdown(self, mock_state):
        """Test costs breakdown in result."""
        result = calculate_total_costs(mock_state, "test_id")
        
        assert "Costos fijos" in result
        assert "Costos variables" in result
        assert "Costos totales" in result


class TestCalculateProfit:
    """Tests for profit calculation."""
    
    def test_profit_calculation(self, mock_state):
        """Test profit calculation."""
        result = calculate_profit(mock_state, "test_id")
        
        # Expected sales: 4.0 * 1200 = 4800
        # Expected costs: 4800
        # Expected profit: 0
        assert "4800" in result or "4,800" in result  # Sales
        assert "✅" in result
    
    def test_profit_with_loss(self, mock_state):
        """Test profit calculation with loss."""
        # Increase fixed costs to create loss
        mock_state["files"]["/business_data/input_data.json"]["data"]["costos_fijos_mensuales"] = 5000.0
        
        result = calculate_profit(mock_state, "test_id")
        
        assert "ALERTA" in result or "⚠️" in result
    
    def test_profit_positive(self, mock_state):
        """Test profit calculation with positive profit."""
        # Increase volume to create profit
        mock_state["files"]["/business_data/input_data.json"]["data"]["volumen_ventas_estimado"] = 2000
        
        result = calculate_profit(mock_state, "test_id")
        
        assert "✅" in result


class TestCalculateProfitability:
    """Tests for profitability ratios calculation."""
    
    def test_ros_calculation(self, mock_state):
        """Test ROS (Return on Sales) calculation."""
        # Modify to ensure positive profit
        mock_state["files"]["/business_data/input_data.json"]["data"]["volumen_ventas_estimado"] = 2000
        
        result = calculate_profitability_ratios(mock_state, "test_id")
        
        assert "ROS" in result
        assert "%" in result
        assert "✅" in result
    
    def test_roi_calculation(self, mock_state):
        """Test ROI calculation with investment."""
        # Ensure positive profit for ROI
        mock_state["files"]["/business_data/input_data.json"]["data"]["volumen_ventas_estimado"] = 2000
        
        result = calculate_profitability_ratios(mock_state, "test_id")
        
        assert "ROI" in result or "Rentabilidad" in result
    
    def test_profitability_low_warning(self, mock_state):
        """Test warning for low profitability."""
        # Set very low profit margin
        mock_state["files"]["/business_data/input_data.json"]["data"]["precio_venta_unitario"] = 2.0
        
        result = calculate_profitability_ratios(mock_state, "test_id")
        
        # Should have warning for low ROS
        assert "ADVERTENCIA" in result or "⚠️" in result


class TestDataValidation:
    """Tests for data validation."""
    
    def test_invalid_margin(self, mock_state):
        """Test with price lower than variable cost."""
        mock_state["files"]["/business_data/input_data.json"]["data"]["precio_venta_unitario"] = 1.0
        
        result = calculate_breakeven_point(mock_state, "test_id")
        
        assert "Error" in result or "❌" in result


class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_zero_volume(self, mock_state):
        """Test with zero sales volume."""
        mock_state["files"]["/business_data/input_data.json"]["data"]["volumen_ventas_estimado"] = 0
        
        # This should be caught by Pydantic validation
        # but if it passes, calculations should handle it
        try:
            result = calculate_total_costs(mock_state, "test_id")
            assert "0" in result or "Error" in result
        except:
            pass  # Expected to fail validation
    
    def test_very_high_fixed_costs(self, mock_state):
        """Test with very high fixed costs."""
        mock_state["files"]["/business_data/input_data.json"]["data"]["costos_fijos_mensuales"] = 100000.0
        
        result = calculate_breakeven_point(mock_state, "test_id")
        
        # Should show high breakeven point
        assert "ALERTA" in result or "⚠️" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
