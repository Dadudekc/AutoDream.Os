import sys, os
sys.path.insert(0, os.getcwd())

import pytest
from src.core.analytics.framework.analytics_engine_core import AnalyticsEngineCore
from src.core.analytics.framework.caching_engine import CachingEngine
from src.core.analytics.framework.analytics_processor import AnalyticsProcessor
from src.core.analytics.framework.analytics_intelligence import AnalyticsIntelligence
from src.core.analytics.framework.predictive_modeling_engine import PredictiveModelingEngine
from src.core.analytics.framework.pattern_analysis_engine import PatternAnalysisEngine
from src.core.analytics.framework.metrics_engine import MetricsEngine
from src.core.analytics.framework.realtime_analytics_engine import RealTimeAnalyticsEngine
from src.core.analytics.framework.analytics_coordinator import AnalyticsCoordinator


def test_caching_engine():
    cache = CachingEngine()
    cache.cache('key', 123)
    assert cache.retrieve('key') == 123
    assert cache.retrieve('missing') is None


def test_module_pass_throughs():
    data = {'value': 1}
    assert AnalyticsProcessor().process(data) == data
    assert AnalyticsIntelligence().run_models(data) == data
    assert PredictiveModelingEngine().forecast(data) == data
    assert PatternAnalysisEngine().detect(data) == data
    assert MetricsEngine().compute(data) == data
    assert isinstance(RealTimeAnalyticsEngine().stream([data]), list)
    coord_data = {
        'processed': data,
        'insights': data,
        'forecast': data,
        'patterns': data,
        'metrics': data,
        'realtime': [data],
    }
    assert AnalyticsCoordinator().coordinate(coord_data) == coord_data


def test_analytics_engine_core_execute():
    core = AnalyticsEngineCore()
    data = {'value': 2}
    result = core.execute(data)
    for key in ['processed', 'insights', 'forecast', 'patterns', 'metrics', 'realtime']:
        assert key in result
    assert result['processed'] == data
    assert isinstance(result['realtime'], list)
