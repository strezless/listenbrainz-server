import sentry_sdk
from flask import Blueprint, jsonify

import listenbrainz.db.user as db_user
from listenbrainz.db.fresh_releases import get_fresh_releases
from listenbrainz.webserver.errors import APINoContent, APINotFound

fresh_releases_bp = Blueprint('fresh_releases_v1', __name__)


@fresh_releases_bp.route("/user/<user_name>/fresh_releases")
def get_releases(user_name):
    """ Get fresh releases data for the given user. """
    user = db_user.get_by_mb_id(user_name)
    if not user:
        raise APINotFound("User %s not found" % user_name)

    try:
        data = get_fresh_releases(user["id"])
        return jsonify({"payload": data})
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise APINoContent('')
