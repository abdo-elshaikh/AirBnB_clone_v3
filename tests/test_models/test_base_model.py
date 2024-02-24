#!/usr/bin/python3
"""Unit tests for BaseModel class"""
import unittest
import os
import json
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test environment"""
        self.model = BaseModel()

    def tearDown(self):
        """Tear down test environment"""
        del self.model
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_init(self):
        """Test initialization of BaseModel instance"""
        self.assertIsInstance(self.model, BaseModel)

    def test_id(self):
        """Test id attribute"""
        self.assertTrue(hasattr(self.model, "id"))
        self.assertIsInstance(self.model.id, str)
        self.assertRegex(self.model.id,
                         r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-"
                         "[a-f0-9]{4}-[a-f0-9]{12}$")

    def test_created_at(self):
        """Test created_at attribute"""
        self.assertTrue(hasattr(self.model, "created_at"))
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at(self):
        """Test updated_at attribute"""
        self.assertTrue(hasattr(self.model, "updated_at"))
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_str(self):
        """Test __str__ method"""
        self.assertIsInstance(str(self.model), str)

    def test_save(self):
        """Test save method"""
        prev_update = self.model.updated_at
        self.model.save()
        self.assertNotEqual(prev_update, self.model.updated_at)

    def test_to_dict(self):
        """Test to_dict method"""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_kwargs(self):
        """Test kwargs input"""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(self.model.id, new_model.id)
        self.assertEqual(self.model.created_at, new_model.created_at)
        self.assertEqual(self.model.updated_at, new_model.updated_at)

    def test_file_storage(self):
        """Test if instances are correctly stored in file storage"""
        self.model.save()
        with open("file.json", "r") as file:
            data = json.load(file)
        key = "{}.{}".format(type(self.model).__name__, self.model.id)
        self.assertEqual(data[key], self.model.to_dict())

    def test_reload(self):
        """Test if instances are correctly loaded from file storage"""
        self.model.save()
        model_id = self.model.id
        del self.model
        new_model = BaseModel()
        new_model.save()
        self.assertNotEqual(model_id, new_model.id)
        BaseModel.reload()
        self.assertTrue(hasattr(BaseModel, model_id))


if __name__ == "__main__":
    unittest.main()
