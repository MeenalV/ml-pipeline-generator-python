# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for models classes."""
import os
import subprocess
import unittest

from ai_pipeline.models import BaseModel
from ai_pipeline.models import SklearnModel


class TestBaseModel(unittest.TestCase):
    """Tests BaseModel class."""

    def test_init(self):
        """Ensure BaseModel is abstract."""
        with self.assertRaises(TypeError):
            BaseModel()


class TestSklearnModel(unittest.TestCase):
    """Tests SklearnModel class."""

    @classmethod
    def setUpClass(cls):
        """Instantiates a model."""
        super(TestSklearnModel, cls).setUpClass()
        cls.config = "examples/sklearn/config.yaml"
        cls.model = SklearnModel(cls.config)

    @classmethod
    def tearDownClass(cls):
        """Cleans up generated directories."""
        super(TestSklearnModel, cls).tearDownClass()
        subprocess.call("./bin/cleanup.sh")

    def test_set_config(self):
        """Ensures instance variables are created."""
        model = self.__class__.model
        model.model = {}

        model._set_config(self.__class__.config)
        self.assertEqual(model.model["name"], "demo_model")

    def test_populate_trainer(self):
        """Ensures task.py and model.py are created."""
        model = self.__class__.model
        # TODO(humichael): support cleaning only training step
        subprocess.call("./bin/cleanup.sh")

        model._populate_trainer()
        trainer_files = os.listdir("trainer")
        bin_files = os.listdir("bin")
        self.assertIn("task.py", trainer_files)
        self.assertIn("model.py", trainer_files)
        self.assertIn("run.train.sh", bin_files)


if __name__ == "__main__":
    unittest.main()