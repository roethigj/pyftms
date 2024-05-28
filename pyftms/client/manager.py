# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from types import MappingProxyType
from typing import Any, cast

from ..models import IndoorBikeSimulationParameters, TrainingStatusCode
from . import const as c
from .backends import FtmsCallback, FtmsEvents, SetupEventData, UpdateEventData
from .properties import MovementDirection


class PropertiesManager:
    """
    Based helper class for `FitnessMachine`. Implements access and caching of
    properties and settings.

    Do not instantinate it.
    """

    _cb: FtmsCallback | None
    """Event Callback function"""

    _properties: UpdateEventData
    """Properties dictonary"""

    _settings: SetupEventData
    """Properties dictonary"""

    _training_status: TrainingStatusCode
    """Last Training Status Code"""

    def __init__(self, on_event_callback: FtmsCallback | None = None) -> None:
        self._cb = on_event_callback
        self._properties = {}
        self._settings = {}

    def set_callback(self, cb: FtmsCallback):
        self._cb = cb

    def _on_event(self, e: FtmsEvents) -> None:
        """Real-time training data update handler."""
        if e.event_id == "update":
            self._properties |= e.event_data
        elif e.event_id == "setup":
            self._settings |= e.event_data
        elif e.event_id == "training_status":
            self._training_status = e.event_data["code"]

        return self._cb and self._cb(e)

    def _get_property(self, name: str) -> Any:
        return self._properties.get(name)

    @property
    def properties(self) -> UpdateEventData:
        """Read-only updateable properties mapping."""
        return cast(UpdateEventData, MappingProxyType(self._properties))

    @property
    def settings(self) -> SetupEventData:
        """Read-only updateable settings mapping."""
        return cast(SetupEventData, MappingProxyType(self._settings))

    @property
    def training_status(self) -> TrainingStatusCode:
        return self._training_status

    # REAL-TIME TRAINING DATA

    @property
    def cadence_average(self) -> float:
        """
        Average Cadence.

        Units: `rpm`.
        """
        return self._get_property(c.CADENCE_AVERAGE)

    @property
    def cadence_instant(self) -> float:
        """
        Instantaneous Cadence.

        Units: `rpm`.
        """
        return self._get_property(c.CADENCE_INSTANT)

    @property
    def distance_total(self) -> int:
        """
        Total Distance.

        Units: `m`.
        """
        return self._get_property(c.DISTANCE_TOTAL)

    @property
    def elevation_gain_negative(self) -> float:
        """
        Negative Elevation Gain.

        Units: `m`.
        """
        return self._get_property(c.ELEVATION_GAIN_NEGATIVE)

    @property
    def elevation_gain_positive(self) -> float:
        """
        Positive Elevation Gain.

        Units: `m`.
        """
        return self._get_property(c.ELEVATION_GAIN_POSITIVE)

    @property
    def energy_per_hour(self) -> int:
        """
        Energy Per Hour.

        Units: `kcal`.
        """
        return self._get_property(c.ENERGY_PER_HOUR)

    @property
    def energy_per_minute(self) -> int:
        """
        Energy Per Minute.

        Units: `kcal`.
        """
        return self._get_property(c.ENERGY_PER_MINUTE)

    @property
    def energy_total(self) -> int:
        """
        Total Energy.

        Units: `kcal`.
        """
        return self._get_property(c.ENERGY_TOTAL)

    @property
    def force_on_belt(self) -> int:
        """
        Force on Belt.

        Units: `newton`.
        """
        return self._get_property(c.FORCE_ON_BELT)

    @property
    def heart_rate(self) -> int:
        """
        Heart Rate.

        Units: `bpm`.
        """
        return self._get_property(c.HEART_RATE)

    @property
    def inclination(self) -> float:
        """
        Inclination.

        Units: `%`.
        """
        return self._get_property(c.INCLINATION)

    @property
    def metabolic_equivalent(self) -> float:
        """
        Metabolic Equivalent.

        Units: `meta`.
        """
        return self._get_property(c.METABOLIC_EQUIVALENT)

    @property
    def movement_direction(self) -> MovementDirection:
        """
        Movement Direction.

        Units: `MovementDirection`.
        """
        return self._get_property(c.MOVEMENT_DIRECTION)

    @property
    def pace_average(self) -> int | float:
        """
        Average Pace.

        Units: `Km/m` or `Seconds(500m)` for `Rower`.
        """
        return self._get_property(c.PACE_AVERAGE)

    @property
    def pace_instant(self) -> int | float:
        """
        Instantaneous Pace.

        Units: `Km/m` or `Seconds(500m)` for `Rower`.
        """
        return self._get_property(c.PACE_INSTANT)

    @property
    def power_average(self) -> int:
        """
        Average Power.

        Units: `Watts`.
        """
        return self._get_property(c.POWER_AVERAGE)

    @property
    def power_instant(self) -> int:
        """
        Instantaneous Power.

        Units: `Watts`.
        """
        return self._get_property(c.POWER_INSTANT)

    @property
    def power_output(self) -> int:
        """
        Power Output.

        Units: `Watts`.
        """
        return self._get_property(c.POWER_OUTPUT)

    @property
    def ramp_angle(self) -> float:
        """
        Ramp Angle Setting.

        Units: `deg`.
        """
        return self._get_property(c.RAMP_ANGLE)

    @property
    def resistance_level(self) -> int | float:
        """
        Resistance Level.

        Units: `unitless`.
        """
        return self._get_property(c.RESISTANCE_LEVEL)

    @property
    def speed_average(self) -> float:
        """
        Average Speed.

        Units: `Km/h`.
        """
        return self._get_property(c.SPEED_AVERAGE)

    @property
    def speed_instant(self) -> float:
        """
        Instantaneous Speed.

        Units: `Km/h`.
        """
        return self._get_property(c.SPEED_INSTANT)

    @property
    def step_rate_average(self) -> int:
        """
        Average Step Rate.

        Units: `step_per_minute`.
        """
        return self._get_property(c.STEP_RATE_AVERAGE)

    @property
    def step_rate_instant(self) -> int:
        """
        Instantaneous Step Rate.

        Units: `step_per_minute`.
        """
        return self._get_property(c.STEP_RATE_INSTANT)

    @property
    def stride_count(self) -> int:
        """
        Stride Count.

        Units: `unitless`.
        """
        return self._get_property(c.STRIDE_COUNT)

    @property
    def stroke_count(self) -> int:
        """
        Stroke Count.

        Units: `unitless`.
        """
        return self._get_property(c.STROKE_COUNT)

    @property
    def stroke_rate_average(self) -> float:
        """
        Average Stroke Rate.

        Units: `stroke/m`.
        """
        return self._get_property(c.STROKE_RATE_AVERAGE)

    @property
    def stroke_rate_instant(self) -> float:
        """
        Instantaneous Stroke Rate.

        Units: `stroke/m`.
        """
        return self._get_property(c.STROKE_RATE_INSTANT)

    @property
    def time_elapsed(self) -> int:
        """
        Elapsed Time.

        Units: `s`.
        """
        return self._get_property(c.TIME_ELAPSED)

    @property
    def time_remaining(self) -> int:
        """
        Remaining Time.

        Units: `s`.
        """
        return self._get_property(c.TIME_REMAINING)

    # SETTINGS

    @property
    def indoor_bike_simulation(self) -> IndoorBikeSimulationParameters:
        """Indoor Bike Simulation Parameters."""
        return self._get_property(c.INDOOR_BIKE_SIMULATION)

    @property
    def target_cadence(self) -> float:
        """
        Targeted cadence.

        Units: `rpm`.
        """
        return self._get_property(c.TARGET_CADENCE)

    @property
    def target_distance(self) -> int:
        """
        Targeted distance.

        Units: `meters`.
        """
        return self._get_property(c.TARGET_DISTANCE)

    @property
    def target_energy(self) -> int:
        """
        Targeted expended energy.

        Units: `kcals`.
        """
        return self._get_property(c.TARGET_ENERGY)

    @property
    def target_heart_rate(self) -> int:
        """
        Targeted heart rate.

        Units: `bpm`.
        """
        return self._get_property(c.TARGET_HEART_RATE)

    @property
    def target_inclination(self) -> float:
        """
        Targeted inclination.

        Units: `%`.
        """
        return self._get_property(c.TARGET_INCLINATION)

    @property
    def target_power(self) -> int:
        """
        Targeted power.

        Units: `Watts`.
        """
        return self._get_property(c.TARGET_POWER)

    @property
    def target_resistance(self) -> float:
        """
        Targeted resistance level.

        Units: `unitless`.
        """
        return self._get_property(c.TARGET_RESISTANCE)

    @property
    def target_speed(self) -> float:
        """
        Targeted speed.

        Units: `km/h`.
        """
        return self._get_property(c.TARGET_SPEED)

    @property
    def target_steps(self) -> int:
        """
        Targeted number of steps.

        Units: `steps`.
        """
        return self._get_property(c.TARGET_STEPS)

    @property
    def target_strides(self) -> int:
        """
        Targeted number of strides.

        Units: `strides`.
        """
        return self._get_property(c.TARGET_STRIDES)

    @property
    def target_time(self) -> tuple[int, ...]:
        """
        Targeted training time.

        Units: `seconds`.
        """
        return self._get_property(c.TARGET_TIME)

    @property
    def wheel_circumference(self) -> float:
        """
        Wheel circumference.

        Units: `mm`.
        """
        return self._get_property(c.WHEEL_CIRCUMFERENCE)