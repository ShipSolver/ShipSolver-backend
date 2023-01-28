import json
import random
import time
from sqlalchemy import create_engine
import inspect as insp
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
import sys
from datetime import datetime

sys.path.insert(0, "..")  # import parent folder

from models.models import TicketStatus
from models.__init__ import session
from utils import convert_dict_to_alchemy_filters


class BaseController:
    def __init__(self, model):
        self.model = model
        self.session = session
        self.primary_key = inspect(self.model).primary_key[0].name

    # def __new__(cls, *args, **kwargs):
    #     if cls is BaseController:
    #         raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
    #     return object.__new__(cls, *args, **kwargs)

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
    def _modify(self, filters: dict, update_dict: dict):

        session_filters = convert_dict_to_alchemy_filters(self.model, filters)
        obj = self.query(self.model).filter(*session_filters).all()
        obj.update(update_dict)

        session.commit()

    # delete an object
    # primary_key_val is the value of the primary key
    def _delete(self, filters=[]):

        objs = (
            session.query(self.model)
            .filter(*convert_dict_to_alchemy_filters(filters))
            .all()
        )

        for obj in objs:
            self.session.delete(obj)

        self.session.commit()

    def _get(self, filters, limit):
        if not filters:
            filters = []

        print("\n\n\n\nPrinting filters:", filters)
        objects = (
            self.session.query(self.model)
            .filter(*convert_dict_to_alchemy_filters(self.model, filters))
            .limit(limit)
            .all()
        )

        return objects

    def _get_count(self, filters):
        if not filters:
            filters = []

        objects = (
            self.session.query(getattr(self.model, self.primary_key))
            .filter(*convert_dict_to_alchemy_filters(self.model, filters))
            .all()
        )

        return len(objects)


class BaseTimeSeriesController(BaseController):
    def __init__(self, model):
        super().__init__(model=model)

        self.model = model  # redudant

    # def __new__(cls, *args, **kwargs):
    #     if cls is BaseTimeSeriesController:
    #         raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
    #     return object.__new__(cls, *args, **kwargs)

    """
    Definition: create an inital object. "args_dict" is the input to models
    """

    def _create_base_event(self, args_dict):
        pass

    def _get_latest_event_objects(self, page=1, number_of_res=1, filters={}):

        # get up to 'number_of_res' last event objects
        # latest_objs = (
        #     self.session.query(self.model)
        #     .filter_by(*convert_dict_to_alchemy_filters(self.model, filters))
        #     .group_by(self.model.non_prim_identifying_column_name)
        #     .order_by(self.model.timestamp)
        #     .limit(number_of_res)
        #     .all()
        # )

        print(*convert_dict_to_alchemy_filters(self.model, filters))
        latest_objs = (
            self.session.query(self.model)
            .distinct(self.model.non_prim_identifying_column_name)
            .filter(*convert_dict_to_alchemy_filters(self.model, filters))
            .order_by(self.model.timestamp)
            .limit(1)
            .all()
        )

        # latest_objs = self.session.query(self.model, subquery).order_by(self.model.timestamp).all()
        print("LATEST_OBJS-------")
        print(latest_objs)
        return latest_objs

    # def _get_latest_event_objects_from_start_date(self, start_datetime, filters={}):

    #     starttime = int(time.mktime(start_datetime).timetuple())

    #     filters.append(self.model.timestamp >= starttime)

    #     latest_objs = (
    #         self.session.query(self.model)
    #         .filter(*convert_dict_to_alchemy_filters(filters))
    #         .group_by(self.model.non_prim_identifying_column_name)
    #         .order_by(self.model.timestamp)
    #     )

    #     return latest_objs

    def _get_latest_event_objects_from_start_date(
        self, datetime1, filters, number_of_res=5
    ):
        return self._get_latest_event_objects_in_range(
            datetime1, datetime.now(), filters=filters, number_of_res=5
        )

    def _get_latest_event_objects_in_range(
        self, datetime1, datetime2, filters={}, number_of_res=5
    ):
        assert datetime1 <= datetime2
        time1 = int(time.mktime(datetime1.timetuple()))
        time2 = int(time.mktime(datetime2.timetuple()))

        session_filters = convert_dict_to_alchemy_filters(self.model, filters)

        session_filters.append(self.model.timestamp >= time1)
        session_filters.append(self.model.timestamp <= time2)

        print(
            "------------------------RUNNING TICKET GET QUERY----------------------------"
        )
        results = (
            self.session.query(self.model)
            .distinct(self.model.non_prim_identifying_column_name)
            .filter(*session_filters)
            .order_by(self.model.non_prim_identifying_column_name, self.model.timestamp)
            .limit(number_of_res)
            .all()
        )
        print("----------complete-----------------")
        for result in results:
            print("TID " + str(result.ticketId))
        return results

    def _find_latest_prim_key_from_non_prim_identifying_column_val(
        self, non_prim_identifying_col_val
    ):
        row = (
            self.session.query(
                getattr(self.model, self.model.non_prim_identifying_column_name),
                self.model.timestamp,
                getattr(self.model, self.primary_key),
            )
            .filter(
                getattr(self.model, self.model.non_prim_identifying_column_name)
                == non_prim_identifying_col_val
            )
            .group_by(
                getattr(self.model, self.model.non_prim_identifying_column_name),
                self.model.timestamp,
                getattr(self.model, self.primary_key),
            )
            .order_by(self.model.timestamp.desc())
            .first(),
        )

        assert (
            len(row) > 0
        ), f"Non-prim identifying ID '{non_prim_identifying_col_val}' for table '{self.model.__tablename__}' is not connected to any events "
        latest_event_id = row[0][2]

        return latest_event_id

    def _modify_latest_object(self, non_prim_identifying_col_val, update_dict):
        """
        Definition: Finds the latest object modified dto instance with a matching
                    non_prim_identifying_column and updates it
        """

        latest_event_id = (
            self._find_latest_prim_key_from_non_prim_identifying_column_val(
                non_prim_identifying_col_val
            )
        )

        latest_obj = (
            self.session.query(self.model)
            .filter(getattr(self.model, self.primary_key) == latest_event_id)
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

    def _modify_object(self, event_id, update_dict):
        """
        Definition: Creates a new event based on the object tied to event_id
        """

        object_to_modify = (
            self.session.query(self.model)
            .filter(getattr(self.model, self.primary_key) == event_id)
            .first()
        )

        row = dict(object_to_modify.__dict__)
        row.pop("_sa_instance_state", None)
        row.pop(self.primary_key, None)
        row.update(update_dict)

        created_obj = self.model(**row)

        self.session.add(created_obj)
        self.session.commit()

        return created_obj


class BaseNestedDependencyContoller(BaseTimeSeriesController):
    def __init__(self, model):
        super().__init__(model=model)

        self.model = model  # redudant

    def __new__(cls, *args, **kwargs):
        if cls is BaseNestedDependencyContoller:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
        return object.__new__(cls, *args, **kwargs)

    def _propagating_modify(
        self, event_id, nested_cls, nested_cls_event_id, update_dict
    ):
        """
        Definition: creates a new shippper event with the same shipperId
                    but creates a new ticketEvent with the updated shipperEventId for
                    the specfic ticket which is given in context
        """

        new_event = self._modify_latest_object(event_id, update_dict)

        nested_controlller = BaseTimeSeriesController(nested_cls)

        nested_controller_update_dict = {
            self.primary_key: getattr(new_event, self.primary_key)
        }

        nested_controlller._modify_object(
            nested_cls_event_id, nested_controller_update_dict
        )

        return new_event
