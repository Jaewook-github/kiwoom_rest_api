# dashboard/app.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dashboard.layouts.main import create_main_layout
from dashboard.callbacks import register_callbacks

def create_app():
    """Dash 애플리케이션 생성"""
    app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    
    app.title = "키움증권 퀀트 투자 대시보드"
    app.layout = create_main_layout()
    
    # 콜백 함수 등록
    register_callbacks(app)
    
    return app
