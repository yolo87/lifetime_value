# Copyright 2019 The Lifetime Value Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Dependency imports

from lifetime_value import metrics
import numpy as np
import pandas as pd
import unittest


class MetricsTest(googletest.TestCase):

  def setUp(self):
    super(MetricsTest, self).setUp()
    n_example = 1000000
    self.y_true = np.arange(n_example, 0., -1.)
    self.y_pred_perfect = np.arange(n_example, 0., -1.)
    self.y_pred_random = np.random.permutation(self.y_pred_perfect)

  def test_gini(self):
    total_value = np.sum(self.y_true)
    cumulative_true = np.cumsum(self.y_true) / total_value
    gain_perfect = metrics.cumulative_true(
        self.y_true, self.y_pred_perfect)
    gain_random = metrics.cumulative_true(
        self.y_true, self.y_pred_random)
    gain = pd.DataFrame({
        'ground_truth': cumulative_true,
        'perfect_model': gain_perfect,
        'random_model': gain_random
    })
    gini = metrics.gini_from_gain(gain)
    self.assertEqual(gini.loc['perfect_model', 'normalized'], 1.)
    self.assertAlmostEqual(gini.loc['random_model', 'normalized'], 0., places=1)

  def test_bucket_stats(self):
    bucket_stats_perfect = metrics.bucket_stats(self.y_true,
                                                self.y_pred_perfect)
    bucket_stats_random = metrics.bucket_stats(self.y_true,
                                               self.y_pred_random)
    self.assertTrue(np.all(bucket_stats_perfect['normalized_rmse'] == 0))
    self.assertTrue(np.all(bucket_stats_perfect['normalized_mae'] == 0))
    self.assertTrue(np.all(bucket_stats_perfect['bucket_mape'] == 0))
    self.assertTrue(
        np.allclose(
            bucket_stats_random['label_mean'],
            np.random.permutation(bucket_stats_random['label_mean']),
            rtol=1e-2,
            atol=1000))


if __name__ == '__main__':
  googletest.main()
