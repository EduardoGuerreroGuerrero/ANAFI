"""
Unit tests for ANAFI scenario analysis tools.

Run with: pytest tests/test_scenarios.py -v
"""
import pytest
from src.tools.scenario_analysis_tools import (
    create_scenario,
    compare_scenarios,
    simulate_parameter_change
)


@pytest.fixture
def sample_business_data():
    """Sample business data for testing."""
    return {
        "nombre_negocio": "Test Shop",
        "tipo_negocio": "tienda",
        "costos_fijos_mensuales": 2000.0,
        "costo_variable_unitario": 5.0,
        "precio_venta_unitario": 15.0,
        "volumen_ventas_estimado": 500,
        "inversion_inicial": 20000.0
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


class TestCreateScenario:
    """Tests for scenario creation."""
    
    def test_create_pessimistic_scenario(self, mock_state):
        """Test pessimistic scenario creation."""
        result = create_scenario("pesimista", None, mock_state, "test_id")
        
        assert "Pesimista" in result
        assert "✅" in result
        assert "/scenarios/scenario_pesimista.json" in mock_state["files"]
    
    def test_create_moderate_scenario(self, mock_state):
        """Test moderate scenario creation."""
        result = create_scenario("moderado", None, mock_state, "test_id")
        
        assert "Moderado" in result
        assert "✅" in result
    
    def test_create_optimistic_scenario(self, mock_state):
        """Test optimistic scenario creation."""
        result = create_scenario("optimista", None, mock_state, "test_id")
        
        assert "Optimista" in result
        assert "✅" in result
    
    def test_create_custom_scenario(self, mock_state):
        """Test custom scenario creation."""
        params = {
            "precio_venta": 20.0,
            "costo_variable": 4.0,
            "volumen_ventas": 600,
            "costos_fijos": 1800.0,
            "nombre": "Escenario Premium"
        }
        
        result = create_scenario("personalizado", params, mock_state, "test_id")
        
        assert "Premium" in result or "Personalizado" in result
        assert "✅" in result
    
    def test_invalid_scenario_type(self, mock_state):
        """Test invalid scenario type."""
        result = create_scenario("invalido", None, mock_state, "test_id")
        
        assert "Error" in result or "❌" in result


class TestCompareScenarios:
    """Tests for scenario comparison."""
    
    def test_compare_two_scenarios(self, mock_state):
        """Test comparing two scenarios."""
        # Create scenarios first
        create_scenario("pesimista", None, mock_state, "test_id")
        create_scenario("optimista", None, mock_state, "test_id")
        
        result = compare_scenarios(["pesimista", "optimista"], mock_state, "test_id")
        
        assert "Comparativa" in result
        assert "✅" in result
    
    def test_compare_three_scenarios(self, mock_state):
        """Test comparing three scenarios."""
        # Create all scenarios
        create_scenario("pesimista", None, mock_state, "test_id")
        create_scenario("moderado", None, mock_state, "test_id")
        create_scenario("optimista", None, mock_state, "test_id")
        
        result = compare_scenarios(["pesimista", "moderado", "optimista"], mock_state, "test_id")
        
        assert "✅" in result
        assert "/scenarios/scenario_analysis.json" in mock_state["files"]
    
    def test_compare_too_many_scenarios(self, mock_state):
        """Test comparing more than 3 scenarios."""
        result = compare_scenarios(["a", "b", "c", "d"], mock_state, "test_id")
        
        assert "Error" in result or "❌" in result
        assert "Máximo 3" in result
    
    def test_compare_too_few_scenarios(self, mock_state):
        """Test comparing less than 2 scenarios."""
        result = compare_scenarios(["pesimista"], mock_state, "test_id")
        
        assert "Error" in result or "❌" in result
    
    def test_compare_nonexistent_scenario(self, mock_state):
        """Test comparing scenario that doesn't exist."""
        result = compare_scenarios(["pesimista", "optimista"], mock_state, "test_id")
        
        assert "Error" in result or "no encontrado" in result


class TestSimulateParameterChange:
    """Tests for parameter change simulation."""
    
    def test_simulate_price_increase(self, mock_state):
        """Test simulating price increase."""
        result = simulate_parameter_change("precio_venta", 10.0, mock_state, "test_id")
        
        assert "Precio de venta" in result
        assert "+10" in result
        assert "✅" in result
    
    def test_simulate_price_decrease(self, mock_state):
        """Test simulating price decrease."""
        result = simulate_parameter_change("precio_venta", -10.0, mock_state, "test_id")
        
        assert "-10" in result
        assert "✅" in result
    
    def test_simulate_cost_change(self, mock_state):
        """Test simulating cost change."""
        result = simulate_parameter_change("costo_variable", 5.0, mock_state, "test_id")
        
        assert "Costo variable" in result
        assert "✅" in result
    
    def test_simulate_volume_change(self, mock_state):
        """Test simulating volume change."""
        result = simulate_parameter_change("volumen_ventas", 20.0, mock_state, "test_id")
        
        assert "Volumen" in result
        assert "✅" in result
    
    def test_simulate_fixed_cost_change(self, mock_state):
        """Test simulating fixed cost change."""
        result = simulate_parameter_change("costo_fijo", -15.0, mock_state, "test_id")
        
        assert "Costos fijos" in result
        assert "✅" in result
    
    def test_simulate_invalid_parameter(self, mock_state):
        """Test simulating invalid parameter."""
        result = simulate_parameter_change("parametro_invalido", 10.0, mock_state, "test_id")
        
        assert "Error" in result or "❌" in result
    
    def test_simulation_saves_to_state(self, mock_state):
        """Test that simulation is saved."""
        simulate_parameter_change("precio_venta", 10.0, mock_state, "test_id")
        
        assert "/scenarios/sensitivity_analysis.json" in mock_state["files"]


class TestScenarioIntegration:
    """Integration tests for scenario analysis."""
    
    def test_full_scenario_workflow(self, mock_state):
        """Test complete scenario analysis workflow."""
        # Create all scenarios
        create_scenario("pesimista", None, mock_state, "test_id")
        create_scenario("moderado", None, mock_state, "test_id")
        create_scenario("optimista", None, mock_state, "test_id")
        
        # Compare them
        compare_result = compare_scenarios(["pesimista", "moderado", "optimista"], mock_state, "test_id")
        
        # Simulate parameter change
        sim_result = simulate_parameter_change("precio_venta", 15.0, mock_state, "test_id")
        
        # All should succeed
        assert "✅" in compare_result
        assert "✅" in sim_result
        
        # All files should be saved
        assert "/scenarios/scenario_pesimista.json" in mock_state["files"]
        assert "/scenarios/scenario_moderado.json" in mock_state["files"]
        assert "/scenarios/scenario_optimista.json" in mock_state["files"]
        assert "/scenarios/scenario_analysis.json" in mock_state["files"]
        assert "/scenarios/sensitivity_analysis.json" in mock_state["files"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
