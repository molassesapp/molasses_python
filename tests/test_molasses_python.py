#!/usr/bin/env python

"""Tests for `molasses_python` package."""

import pytest

from molasses import MolassesClient

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
                "id": "1",
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
                "id": "1",
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
                "id": "1",
                "active": True,
                "description": "foo",
                "key": "FOO_TEST",
                "segments": [],
            },
            {
                "id": "2",
                "active": False,
                "description": "foo",
                "key": "FOO_FALSE_TEST",
                "segments": [],
            },
            {
                "id": "3",
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
                "id": "4",
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
                "id": "5",
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
    responses.add(responses.GET, 'https://sdk.molasses.app/v1/features',
                  json=responseA, status=200)

    molasses = MolassesClient("test_key",  send_events=False)
    assert molasses.is_active("FOO_TEST") is True
    assert molasses.is_active("FOO_TEST", {"foo": "foo"}) is True
    assert molasses.is_active("NOT_CHECKOUT") is False
    assert molasses.is_active("FOO_TEST", {"id": "foo", "params": {}}) is True
    assert molasses.is_active("FOO_TEST", {"id": "food", "params": {
                              "isScaredUser": "true"}}) is False
    assert molasses.is_active("FOO_TEST", {"id": "foodie", "params": {
                              "isBetaUser": "true"}}) is True


@responses.activate
def test_more_advanced():
    responses.add(responses.GET, 'https://sdk.molasses.app/v1/features',
                  json=responseB, status=200)

    molasses = MolassesClient("test_key",  send_events=False)
    assert molasses.is_active("FOO_TEST") is True
    assert molasses.is_active("FOO_TEST", {"foo": "foo"}) is True
    assert molasses.is_active("NOT_CHECKOUT") is False
    assert molasses.is_active("FOO_TEST", {"id": "foo", "params": {
                              "isBetaUser": "false", "isScaredUser": "false"}}) is True
    assert molasses.is_active("FOO_TEST", {"id": "food", "params": {
                              "isScaredUser": "true"}}) is False
    assert molasses.is_active("FOO_TEST", {"id": "foodie", "params": {
                              "isBetaUser": "true"}}) is True


@responses.activate
def test_even_more_advanced():
    responses.add(responses.GET, 'https://sdk.molasses.app/v1/features',
                  json=responseC, status=200)

    molasses = MolassesClient("test_key",  send_events=False)
    assert molasses.is_active("FOO_TEST", {"id": "foo", "params": {
        "isScaredUser": "scared",
        "isDefinitelyScaredUser": "scared",
        "isMostDefinitelyScaredUser": "scared",
    }}) is False
    assert molasses.is_active("FOO_TEST", {"id": "food", "params": {
                              "isDefinitelyBetaUser": "true", "isBetaUser": "true"}}) is True
    assert molasses.is_active("FOO_TEST", {"id": "foodie", "params": {
                              "isBetaUser": "true"}}) is True


@responses.activate
def test_percentage_tests():
    responses.add(responses.GET, 'https://sdk.molasses.app/v1/features',
                  json=responseD, status=200)

    molasses = MolassesClient("test_key", send_events=False)
    assert molasses.is_active("FOO_TEST") is True
    assert molasses.is_active("FOO_FALSE_TEST") is False
    assert molasses.is_active("FOO_50_PERCENT_TEST", {
                              "id": "140", "params": {}}) is False
    assert molasses.is_active("FOO_50_PERCENT_TEST", {
                              "id": "123", "params": {}}) is True
    assert molasses.is_active("FOO_0_PERCENT_TEST", {
        "id": "123", "params": {}}) is False
    assert molasses.is_active("FOO_ID_TEST", {
        "id": "123", "params": {}}) is False
    assert molasses.is_active("FOO_ID_TEST", {
        "id": "124", "params": {}}) is True
    assert molasses.is_active("FOO_ID_TEST", {
        "id": "122", "params": {}}) is True


@responses.activate
def test_experiments():
    responses.add(responses.GET, 'https://sdk.molasses.app/v1/features',
                  json=responseD, status=200)
    responses.add(responses.POST, 'https://sdk.molasses.app/v1/analytics',
                  json={}, status=200)

    molasses = MolassesClient("test_key", send_events=True)
    assert molasses.is_active("FOO_TEST") is True
    assert molasses.is_active("FOO_FALSE_TEST") is False
    assert molasses.is_active("FOO_50_PERCENT_TEST", {
                              "id": "140", "params": {}}) is False
    molasses.experiment_success("FOO_50_PERCENT_TEST", {}, {
        "id": "140", "params": {}})
    assert molasses.is_active("FOO_50_PERCENT_TEST", {
                              "id": "123", "params": {}}) is True
    molasses.experiment_success("FOO_50_PERCENT_TEST", {}, {
        "id": "123", "params": {}})
