
import unittest

import numpy as np
import pandas as pd

from src.cri_calculator import (
    bounded_score,
    mean_available,
    calculate_row,
)
from src.feature_extraction import interval_features, cognitive_features


class TestCRIScoring(unittest.TestCase):
    def test_bounded_score_midpoint(self):
        self.assertAlmostEqual(bounded_score(45, 20, 70), 50.0)

    def test_bounded_score_clips_low_and_high(self):
        self.assertEqual(bounded_score(10, 20, 70), 0.0)
        self.assertEqual(bounded_score(80, 20, 70), 100.0)

    def test_bounded_score_missing_or_invalid_range(self):
        self.assertTrue(np.isnan(bounded_score(np.nan, 20, 70)))
        self.assertTrue(np.isnan(bounded_score(30, 20, 20)))

    def test_mean_available_ignores_missing_values(self):
        self.assertEqual(mean_available([20.0, np.nan, 60.0]), 40.0)

    def test_mean_available_empty_values(self):
        self.assertTrue(np.isnan(mean_available([np.nan, np.nan])))

    def test_calculate_row_complete_data(self):
        row = pd.Series({
            "rmssd_ms": 45.0,
            "sdnn_ms": 45.0,
            "nback_accuracy_pct": 80.0,
            "nback_median_rt_ms": 525.0,
            "gsr_mean_raw": 2.5,
            "gsr_unit": "example_unit",
            "accel_dynamic_rms_g": 0.03,
            "signal_quality_mean": 0.95,
        })

        result = calculate_row(row)

        # Both variability scores: 50.
        self.assertAlmostEqual(
            result["physiology_score_experimental"], 50.0
        )

        # Accuracy: 80; reaction time: 50.
        # Cognitive score = 0.70 * 80 + 0.30 * 50 = 71.
        self.assertAlmostEqual(
            result["cognitive_score_experimental"], 71.0
        )

        # CRI = 0.50 * 50 + 0.50 * 71 = 60.5.
        self.assertAlmostEqual(result["cri_experimental"], 60.5)
        self.assertEqual(
            result["score_status"], "Experimental; requires validation"
        )

    def test_calculate_row_does_not_fill_missing_component_with_zero(self):
        row = pd.Series({
            "rmssd_ms": 40.0,
            "sdnn_ms": 45.0,
            "nback_accuracy_pct": 80.0,
            "nback_median_rt_ms": np.nan,
        })

        result = calculate_row(row)

        self.assertTrue(
            np.isnan(result["cognitive_score_experimental"])
        )
        self.assertTrue(np.isnan(result["cri_experimental"]))

    def test_calculate_row_requires_both_cognitive_measures(self):
        row = pd.Series({
            "rmssd_ms": 45.0,
            "sdnn_ms": 45.0,
            "nback_accuracy_pct": 80.0,
            "nback_median_rt_ms": np.nan,
        })

        result = calculate_row(row)
        self.assertTrue(
            np.isnan(result["cognitive_score_experimental"])
        )

    def test_calculate_row_retains_gsr_as_separate_indicator(self):
        row = pd.Series({
            "rmssd_ms": 45.0,
            "sdnn_ms": 45.0,
            "nback_accuracy_pct": 80.0,
            "nback_median_rt_ms": 525.0,
            "gsr_mean_raw": 2.5,
            "gsr_unit": "example_unit",
        })

        result = calculate_row(row)
        self.assertEqual(result["gsr_mean_raw"], 2.5)
        self.assertEqual(result["gsr_unit"], "example_unit")


class TestIntervalFeatures(unittest.TestCase):
    def test_interval_features_with_valid_values(self):
        result = interval_features(pd.Series([800, 810, 820]))

        self.assertEqual(result["interval_count"], 3)
        self.assertAlmostEqual(result["rmssd_ms"], np.sqrt(150))
        self.assertAlmostEqual(result["sdnn_ms"], 10.0)

    def test_interval_features_filters_out_of_range_values(self):
        result = interval_features(pd.Series([200, 800, 810, 3000]))

        self.assertEqual(result["interval_count"], 2)
        self.assertTrue(np.isnan(result["rmssd_ms"]))
        self.assertTrue(np.isnan(result["sdnn_ms"]))

    def test_interval_features_requires_at_least_three_values(self):
        result = interval_features(pd.Series([800, 810]))

        self.assertEqual(result["interval_count"], 2)
        self.assertTrue(np.isnan(result["rmssd_ms"]))
        self.assertTrue(np.isnan(result["sdnn_ms"]))


class TestCognitiveFeatures(unittest.TestCase):
    def test_cognitive_hits_misses_false_alarms_and_accuracy(self):
        group = pd.DataFrame({
            "is_target": [1, 1, 0, 0],
            "response_made": [1, 0, 1, 0],
            "correct": [1, 0, 0, 1],
            "reaction_time_ms": [400, 500, 450, 0],
        })

        result = cognitive_features(group)

        self.assertEqual(result["nback_trials"], 4)
        self.assertEqual(result["nback_hits"], 1)
        self.assertEqual(result["nback_misses"], 1)
        self.assertEqual(result["nback_false_alarms"], 1)
        self.assertAlmostEqual(result["nback_accuracy_pct"], 50.0)
        self.assertAlmostEqual(result["nback_median_rt_ms"], 450.0)

    def test_cognitive_features_without_required_columns(self):
        group = pd.DataFrame({"reaction_time_ms": [400, 500]})

        result = cognitive_features(group)

        self.assertEqual(result["nback_trials"], 2)
        self.assertTrue(np.isnan(result["nback_accuracy_pct"]))


if __name__ == "__main__":
    unittest.main()
