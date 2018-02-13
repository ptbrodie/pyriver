from flask import Blueprint, jsonify, request

from pyriver.services import river_service, event_service
from pyriver.models import River


bp = Blueprint("api", __name__)


@bp.route("/rivers")
def get_rivers():
    rivers = River.query.all()
    schemas = []
    for river in rivers:
        schemas.append(river_service.to_doc(river))
    return jsonify(rivers=schemas)


@bp.route("/rivers/<river_id>")
def get_river(river_id):
    river = river_service.get_by_id(river_id)
    if river:
        return jsonify(river=river_service.to_doc(river))
    return "River %s not found." % river_id, 404


@bp.route("/rivers/<river_id>/events")
def get_events(river_id):
    river = river_service.get_by_id(river_id)
    if not river:
        return "River %s not found." % river_id, 404
    page = request.args.get("page", 0)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    events = event_service.get_events(river, page, start_date, end_date)
    result = []
    for event in events:
        result.append(event_service.to_doc(event))
    return jsonify(events=result)
