#!/usr/bin/env python

"""Tests for `molasses_python` package."""

import pytest

from molasses_python import MolassesClient

import responses

responseA = {
    "data": {
        "features": [
            {
                "active": True,
                "description": "foo",
                "key": "FOO_TEST",
                "segments": [
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "alwaysControl",
                        "userConstraints": [
                            {
                                "userParam": "isScaredUser",
                                "operator": "in",
                                "values": "true,maybe",
                            },
                        ],
                    },
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "alwaysExperiment",
                        "userConstraints": [
                            {
                                "userParam": "isBetaUser",
                                "operator": "equals",
                                "values": "true",
                            },
                        ],
                    },
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "everyoneElse",
                        "userConstraints": [],
                    },
                ],
            },
        ],
    }, }
responseB = {
    "data": {
        "features": [
            {
                "active": True,
                "description": "foo",
                "key": "FOO_TEST",
                "segments": [
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "alwaysControl",
                        "userConstraints": [
                            {
                                "userParam": "isScaredUser",
                                "operator": "nin",
                                "values": "false,maybe",
                            },
                        ],
                    },
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "alwaysExperiment",
                        "userConstraints": [
                            {
                                "userParam": "isBetaUser",
                                "operator": "doesNotEqual",
                                "values": "false",
                            },
                        ],
                    },
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "everyoneElse",
                        "userConstraints": [],
                    },
                ],
            },
        ],
    },
}

responseC = {
    "data": {
        "features": [
            {
                "active": True,
                "description": "foo",
                "key": "FOO_TEST",
                "segments": [
                    {
                        "percentage": 100,
                        "segmentType": "alwaysControl",
                        "constraint": "all",
                        "userConstraints": [
                            {
                                "userParam": "isScaredUser",
                                "operator": "contains",
                                "values": "scared",
                            },
                            {
                                "userParam": "isDefinitelyScaredUser",
                                "operator": "contains",
                                "values": "scared",
                            },
                            {
                                "userParam": "isMostDefinitelyScaredUser",
                                "operator": "contains",
                                "values": "scared",
                            },
                        ],
                    },
                    {
                        "percentage": 100,
                        "segmentType": "alwaysExperiment",
                        "constraint": "any",
                        "userConstraints": [
                            {
                                "userParam": "isBetaUser",
                                "operator": "doesNotContain",
                                "values": "fal",
                            },
                            {
                                "userParam": "isDefinitelyBetaUser",
                                "operator": "doesNotContain",
                                "values": "fal",
                            },
                        ],
                    },
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "everyoneElse",
                        "userConstraints": [],
                    },
                ],
            },
        ],
    },
}

responseD = {
    "data": {
        "features": [
            {
                "active": True,
                "description": "foo",
                "key": "FOO_TEST",
                "segments": [],
            },
            {
                "active": False,
                "description": "foo",
                "key": "FOO_FALSE_TEST",
                "segments": [],
            },
            {
                "active": True,
                "description": "foo",
                "key": "FOO_50_PERCENT_TEST",
                "segments": [
                    {
                        "constraint": "all",
                        "segmentType": "everyoneElse",
                        "percentage": 50,
                        "userConstraints": [],
                    },
                ],
            },
            {
                "active": True,
                "description": "foo",
                "key": "FOO_0_PERCENT_TEST",
                "segments": [
                    {
                        "constraint": "all",
                        "segmentType": "everyoneElse",
                        "percentage": 0,
                        "userConstraints": [],
                    },
                ],
            },
            {
                "active": True,
                "description": "foo",
                "key": "FOO_ID_TEST",
                "segments": [
                    {
                        "constraint": "all",
                        "percentage": 100,
                        "segmentType": "alwaysControl",
                        "userConstraints": [
                            {
                                "userParam": "id",
                                "operator": "equals",
                                "values": "123",
                            },
                        ],
                    },
                    {
                        "constraint": "all",
                        "segmentType": "everyoneElse",
                        "percentage": 100,
                        "userConstraints": [],
                    },
                ],
            },
        ],
    },
}


@responses.activate
def test_basic():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    responses.add(responses.GET, 'https://us-central1-molasses-36bff.cloudfunctions.net/get-features',
                  json=responseA, status=200)

    molasses = MolassesClient("test_key")
    assert molasses.is_active("FOO_TEST") == True
    assert molasses.is_active("FOO_TEST", {"foo": "foo"}) == True
    assert molasses.is_active("NOT_CHECKOUT") == False
    assert molasses.is_active("FOO_TEST", {"id": "foo", "params": {}}) == True
    assert molasses.is_active("FOO_TEST", {"id": "food", "params": {
                              "isScaredUser": "true"}}) == False
    assert molasses.is_active("FOO_TEST", {"id": "foodie", "params": {
                              "isBetaUser": "true"}}) == True


@responses.activate
def test_more_advanced():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    responses.add(responses.GET, 'https://us-central1-molasses-36bff.cloudfunctions.net/get-features',
                  json=responseB, status=200)

    molasses = MolassesClient("test_key")
    assert molasses.is_active("FOO_TEST") == True
    assert molasses.is_active("FOO_TEST", {"foo": "foo"}) == True
    assert molasses.is_active("NOT_CHECKOUT") == False
    assert molasses.is_active("FOO_TEST", {"id": "foo", "params": {
                              "isBetaUser": "false", "isScaredUser": "false"}}) == True
    assert molasses.is_active("FOO_TEST", {"id": "food", "params": {
                              "isScaredUser": "true"}}) == False
    assert molasses.is_active("FOO_TEST", {"id": "foodie", "params": {
                              "isBetaUser": "true"}}) == True


@responses.activate
def test_even_more_advanced():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')
    responses.add(responses.GET, 'https://us-central1-molasses-36bff.cloudfunctions.net/get-features',
                  json=responseC, status=200)

    molasses = MolassesClient("test_key")
    assert molasses.is_active("FOO_TEST", {"id": "foo", "params": {
        "isScaredUser": "scared",
        "isDefinitelyScaredUser": "scared",
        "isMostDefinitelyScaredUser": "scared",
    }}) == False
    assert molasses.is_active("FOO_TEST", {"id": "food", "params": {
                              "isDefinitelyBetaUser": "true", "isBetaUser": "true"}}) == True
    assert molasses.is_active("FOO_TEST", {"id": "foodie", "params": {
                              "isBetaUser": "true"}}) == True


@responses.activate
def test_percentage_tests():
    responses.add(responses.GET, 'https://us-central1-molasses-36bff.cloudfunctions.net/get-features',
                  json=responseD, status=200)

    molasses = MolassesClient("test_key")
    assert molasses.is_active("FOO_TEST") == True
    assert molasses.is_active("FOO_FALSE_TEST") == False
    assert molasses.is_active("FOO_50_PERCENT_TEST", {
                              "id": "140", "params": {}}) == False
    assert molasses.is_active("FOO_50_PERCENT_TEST", {
                              "id": "123", "params": {}}) == True
    assert molasses.is_active("FOO_0_PERCENT_TEST", {
        "id": "123", "params": {}}) == False
    assert molasses.is_active("FOO_ID_TEST", {
        "id": "123", "params": {}}) == False
    assert molasses.is_active("FOO_ID_TEST", {
        "id": "124", "params": {}}) == True
    assert molasses.is_active("FOO_ID_TEST", {
        "id": "122", "params": {}}) == True
