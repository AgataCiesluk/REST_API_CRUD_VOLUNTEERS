from sqlalchemy import exc

from exceptions import NoRecordFound
from models import Volunteer
from utils import models_list_to_dict


def db_add_volunteer(first_name, last_name, phone_number, db_model):
    volunteer = Volunteer(first_name, last_name, phone_number)
    db_model.session.add(volunteer)
    db_model.session.commit()
    return volunteer


def db_delete_volunteer(id, db_model):
    try:
        volunteer = get_volunteer_by_id(id)
    except NoRecordFound:
        raise
    db_model.session.delete(volunteer)
    db_model.session.commit()
    return volunteer


def db_update_volunteer(id, db_model, first_name=None, last_name=None, phone_number=None):
    try:
        volunteer = get_volunteer_by_id(id)
    except NoRecordFound:
        raise
    if first_name:  # TODO: methods to validate first_name
        volunteer.first_name = first_name
    if last_name:  # TODO: methods to validate last_name
        volunteer.last_name = last_name
    if phone_number:  # TODO: methods to validate phone_number
        volunteer.phone_number = phone_number
    db_model.session.flush()
    db_model.session.commit()
    return volunteer


def get_all_volunteers():
    all_volunteers = Volunteer.query.all()
    return models_list_to_dict(all_volunteers)


def get_volunteer_by_id(volunteer_id: int):
    try:
        volunteer = Volunteer.query.filter_by(volunteer_id=volunteer_id).one()
    except exc.NoResultFound as e:
        #     TODO: Logger with original error message logger.warning(e.message)
        raise NoRecordFound
    return volunteer
