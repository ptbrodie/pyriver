from flask import Blueprint

from pyriver.services.river_service import RiverService
from pyriver.models import River


bp = Blueprint("api", __name__)


@bp.route("/rivers")
def get_rivers():
    rivers = River.query.all()
    schemas = []
    for river in rivers:
        schemas.append(river.schema)
    return jsonify(rivers=schemas)


@bp.route("/rivers/<river_id>")
def get_river(river_id):
    pass


@bp.route("/rivers/<river_id>/events")
def get_events(river_id):
    river = RiverService.get_by_id(river_id)
    if not river:
        return "River %s not found." % river_id, 404
    page = request.json.get("page", 0)
    start_date = request.json.get("start_date")
    end_date = request.json.get("end_date")
    events = EventService.get_events(river, page, start_date, end_date)
