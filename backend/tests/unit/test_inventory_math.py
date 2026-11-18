from datetime import date
import pytest
from liquor_pos.core.domain.entities.batch import Batch
from liquor_pos.core.domain.exceptions.base import NegativeStockError

def test_batch_deduct_stock_success():
    batch = Batch(id="1", product_id="P1", batch_number="L1", expiration_date=date(2027, 1, 1), stock_base_units=100)
    batch.deduct_stock(10)
    assert batch.stock_base_units == 90

def test_batch_deduct_stock_fails_negative():
    batch = Batch(id="1", product_id="P1", batch_number="L1", expiration_date=date(2027, 1, 1), stock_base_units=5)
    with pytest.raises(NegativeStockError):
        batch.deduct_stock(10)

def test_batch_add_stock():
    batch = Batch(id="1", product_id="P1", batch_number="L1", expiration_date=date(2027, 1, 1), stock_base_units=50)
    batch.add_stock(20)
    assert batch.stock_base_units == 70
