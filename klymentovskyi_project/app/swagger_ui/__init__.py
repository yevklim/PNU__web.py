from flask_swagger_ui import get_swaggerui_blueprint

swagger_ui_blueprint = get_swaggerui_blueprint(
    base_url='/swagger',
    api_url='/base/static/swagger.json',
)
