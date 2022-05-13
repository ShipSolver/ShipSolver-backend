import json
import random
import time
from sqlalchemy import create_engine
import inspect as insp
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
import sys

sys.path.insert(0, "..")  # import parent folder

from models.models import Users
from models.__init__ import session


class BaseController:
    def __init__(self, model):
        self.model = model
        self.session = session
        self.primary_key = inspect(self.model).primary_key[0].name

    # create objects in bulk
    # args_arr is an array of args_dicts
    # args_dict is the input to models
    def _create_bulk(self, args_arr):  # this does not create objs (need to commit)

        assert isinstance(args_arr, list)

        prim_ids = []

        for args_dict in args_arr:
            assert isinstance(args_dict, dict)

            obj = self.model(**args_dict)
            self.session.add(obj)
            prim_ids.append(getattr(obj, self.primary_key))

        self.session.commit()

        return prim_ids

    # create objects in bulk
    # args_dict is the input to models
    def _create(self, args_dict):  # this does not create objs (need to commit)

        assert isinstance(args_dict, dict)

        obj = self.model(**args_dict)
        self.session.add(obj)
        self.session.commit()
        return obj

    # update an object
    # primary_key_val is the value of the primary key
    # update_dict is a subset of the models args_dict
    def _modify(self, primary_key_val, update_dict):

        obj = (
            self.query(self.model)
            .filter(getattr(self.model, self.primary_key) == primary_key_val)
            .first()
        )
        obj.update(update_dict)

        session.commit()

    # delete an object
    # primary_key_val is the value of the primary key
    def _delete(self, primary_key_val):

        objs = (
            session.query(self.model)
            .filter(getattr(self.model, self.primary_key) == primary_key_val)
            .all()
        )

        for obj in objs:
            self.session.delete(obj)

        self.session.commit()


class BaseTimeSeriesController(BaseController):
    def __init__(self, model):
        super().__init__(model=model)

        self.model = model  # redudant

    # create an inital object
    # args_dict is the input to models
    def _create_base_event(self, args_dict):

        id = random.randint(1, 2147483640)

        args_dict[self.primary_key] = id
        args_dict[self.model.non_prim_identifying_column_name] = id

        obj = self.model(**args_dict)
        self.session.add(obj)
        self.session.commit()

        return obj

    # get up to 'number_of_res' last event objects
    def _get_latest_event_objects(self, number_of_res):

        latest_objs = (
            self.session.query(self.model)
            .group_by(self.model.non_prim_identifying_column_name)
            .order_by(self.model.timestamp)
        ).limit(number_of_res)

        return latest_objs

    def _get_latest_event_objects_from_start_date(self, start_datetime):

        starttime = int(time.mktime(start_datetime).timetuple())

        latest_objs = (
            self.session.query(self.model)
            .filter(self.model.timestamp >= starttime)
            .group_by(self.model.non_prim_identifying_column_name)
            .order_by(self.model.timestamp)
        )

        return latest_objs

    def _get_latest_event_objects_in_range(self, datetime1, datetime2):

        assert datetime1 <= datetime2

        time1 = int(time.mktime(datetime1.timetuple()))
        time2 = int(time.mktime(datetime2.timetuple()))

        results = (
            self.session.query(self.model)
            .filter(self.model.timestamp >= time1, self.model.timestamp <= time2)
            .all()
        )

        return results

    def _get_latest_event_objects_in_range_with_limit(
        self, datetime1, datetime2, max_number_of_results=None
    ):

        assert datetime1 <= datetime2

        time1 = int(time.mktime(datetime1.timetuple()))
        time2 = int(time.mktime(datetime2.timetuple()))

        if max_number_of_results is None:
            latest_objs = (
                self.session.query(self.model)
                .filter(self.model.timestamp >= time1, self.model.timestamp <= time2)
                .group_by(self.model.non_prim_identifying_column_name)
                .order_by(self.model.timestamp)
            ).all()

        elif isinstance(max_number_of_results, int):
            latest_objs = (
                self.session.query(self.model)
                .filter(self.model.timestamp >= time1, self.model.timestamp <= time2)
                .group_by(self.model.non_prim_identifying_column_name)
                .order_by(self.model.timestamp)
            ).limit(max_number_of_results)

        return latest_objs

    def _modify_object(self, non_prim_identifying_column_name, update_dict):
        # this functions finds the latest object modified dto instance
        # with a matching non_prim_identifying_column and updates it

        row = (
            self.session.query(
                getattr(self.model, self.model.non_prim_identifying_column_name),
                self.model.timestamp,
                getattr(self.model, self.primary_key),
            )
            .filter(
                getattr(self.model, self.model.non_prim_identifying_column_name)
                == non_prim_identifying_column_name
            )
            .group_by(
                getattr(self.model, self.model.non_prim_identifying_column_name),
                self.model.timestamp,
                getattr(self.model, self.primary_key),
            )
            .order_by(self.model.timestamp.desc())
            .first(),
        )

        latest_prim_key = row[0][2]

        latest_obj = (
            self.session.query(self.model)
            .filter(getattr(self.model, self.primary_key) == latest_prim_key)
            .first()
        )

        row = dict(latest_obj.__dict__)
        row.pop("_sa_instance_state", None)
        row.pop(self.primary_key, None)
        row.update(update_dict)

        obj = self.model(**row)

        self.session.add(obj)
        self.session.commit()

        return obj
