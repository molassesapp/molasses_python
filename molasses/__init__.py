"""Top-level package for molasses."""

__author__ = """James Hrisho"""
__email__ = 'james.hrisho@gmail.com'
__version__ = '0.1.2'

import logging
import requests
import zlib
import json
from typing import Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
logger = logging.getLogger(__name__)

BASE_URL = 'https://sdk.molasses.app/v1'


class MolassesClient:
    """
    docstring
    """
    __cache = {}
    __initialized = False

    def __init__(self, api_key: str, send_events=True, base_url=BASE_URL):
        self.api_key = api_key
        self.send_events = send_events
        self.base_url = base_url
        self.__fetch_features()
        self.scheduler = BackgroundScheduler()
        self.features_job = self.scheduler.add_job(self.__fetch_features,
                                                   trigger=IntervalTrigger(seconds=int(15)))
        self.scheduler.start()

    def is_active(self, key: str, user: Optional[Dict] = None):
        if self.__initialized is not True:
            return False

        if key in self.__cache:
            feature = self.__cache[key]
            result = self.__is_active(feature, user)
            if user and "id" in user and self.send_events:
                self.__send_events({
                    "event": "experiment_started",
                    "tags": user["params"],
                    "userId": user["id"],
                    "featureId": feature["id"],
                    "featureName": key,
                    "testType": result if "experiment" else "control"
                })
            return result
        else:
            return False

    def experiment_success(self, key: str, additional_details: Dict, user: Optional[Dict] = None):
        if self.__initialized is not True or self.send_events is not True or user is None or "id" not in user:
            return False
        feature = self.__cache[key]
        result = self.__is_active(feature, user)
        self.__send_events({
            "event": "experiment_success",
            "tags": {**user["params"], **additional_details},
            "userId": user["id"],
            "featureId": feature["id"],
            "featureName": key,
            "testType": result if "experiment" else "control"
        })

    def stop(self):
        self.features_job.stop()
        self.scheduler.shutdown()

    def __is_active(self, feature, user=None):
        if feature["active"] is not True:
            return False
        if user is None or "id" not in user:
            return True
        segment_map = {}
        for feature_segment in feature["segments"]:
            segment_type = feature_segment["segmentType"]
            segment_map[segment_type] = feature_segment
        if "alwaysControl" in segment_map and self.__is_user_in_segment(user, segment_map["alwaysControl"]):
            return False
        if "alwaysExperiment" in segment_map and self.__is_user_in_segment(user, segment_map["alwaysExperiment"]):
            return True
        if "everyoneElse" in segment_map:
            return self.__get_user_percentage(user["id"], segment_map["everyoneElse"]["percentage"])
        return False

    def __get_user_percentage(self, id="", percentage=0):
        if percentage == 100:
            return True
        if percentage == 0:
            return False
        c = zlib.crc32(bytes(id, "utf-8")) & 0xffffffff
        v = abs(c % 100)
        return v < percentage

    def __is_user_in_segment(self, user: Optional[Dict], s: Dict):
        user_constraints = s["userConstraints"]
        constraints_length = len(user_constraints)
        constraints_to_be_met = 1 if s["constraint"] == "any" else constraints_length
        constraints_met = 0

        for i in range(constraints_length):
            constraint = user_constraints[i]
            param = constraint["userParam"]
            param_exists = param in user["params"]
            user_value = None
            if param_exists:
                user_value = user["params"][param]
            if param == "id":
                param_exists = True
                user_value = user["id"]
            if self.__meets_constraint(user_value, param_exists, constraint):
                constraints_met = constraints_met + 1
        return constraints_met >= constraints_to_be_met

    def __meets_constraint(self, user_value, param_exists, constraint):
        operator = constraint["operator"]
        if param_exists is False:
            return False
        if operator == "in":
            list_values = constraint["values"].split(",")
            return user_value in list_values
        elif operator == "nin":
            list_values = constraint["values"].split(",")
            return user_value not in list_values
        elif operator == "equals":
            return user_value == constraint["values"]
        elif operator == "doesNotEqual":
            return user_value != constraint["values"]
        elif operator == "contains":
            return user_value in constraint["values"]
        elif operator == "doesNotContain":
            return user_value not in constraint["values"]
        else:
            return False

    def __send_events(self, event_options: Dict):
        event_options["tags"] = json.dumps(event_options["tags"])
        requests.post(self.base_url + "/analytics", json=event_options, headers={
            "Authorization": "Bearer " + self.api_key
        })

    def __fetch_features(self):
        response = requests.get(self.base_url + "/features", params={}, headers={
            "Authorization": "Bearer " + self.api_key
        })
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                d = data.get("data")
                if "features" in d:
                    features = d.get("features")
                    for feature in features:
                        self.__cache[feature["key"]] = feature
                    self.__initialized = True
        else:
            logger.error("Molasses - %s %s",
                         response.status_code, response.text, exc_info=1)
