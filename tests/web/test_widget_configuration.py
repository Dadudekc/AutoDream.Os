from src.services.dashboard import (
    DashboardFrontend,
    DashboardWidget,
    ChartType,
)


def test_widget_configuration_modal_and_persistence():
    frontend = DashboardFrontend()
    widget = DashboardWidget(
        widget_id="w1", title="Test", chart_type=ChartType.LINE, metric_name="m1"
    )
    frontend.add_widget(widget)
    html = frontend.generate_html()
    assert "config-modal-w1" in html
    assert "localStorage.setItem" in html
