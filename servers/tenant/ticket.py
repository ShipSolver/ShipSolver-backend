from flask import request, jsonify, Blueprint
from tenant import ticket_bp


@ticket_bp.route("", methods=["POST"])
def ticket_post():  # create ticket
    pass


@ticket_bp.route("", methods=["GET"])
def ticket_get_range():
    # require a range of tickets aggregated
    pass


@ticket_bp.route("{ticket_id}", methods=["GET"])
def ticket_get():
    # specific ticket + milestones
    pass
