import pytest
import uuid
from src.utils.set_joins import join_sets_with_common_elements

@pytest.mark.asyncio
def test_set_joins():
    # Create some UUIDs for testing
    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    id3 = uuid.uuid4()
    id4 = uuid.uuid4()
    id5 = uuid.uuid4()
    
    # Test case 1: Two sets with one common element
    sets1 = [
        {id1, id2},
        {id2, id3}
    ]
    result1 = join_sets_with_common_elements(sets1)
    assert len(result1) == 1
    assert result1[0] == {id1, id2, id3}
    
    # Test case 2: Three sets that should all merge
    sets2 = [
        {id1, id2},
        {id2, id3},
        {id3, id4}
    ]
    result2 = join_sets_with_common_elements(sets2)
    assert len(result2) == 1
    assert result2[0] == {id1, id2, id3, id4}
    
    # Test case 3: Two separate groups
    sets3 = [
        {id1, id2},
        {id2, id3},
        {id4, id5}
    ]
    result3 = join_sets_with_common_elements(sets3)
    assert len(result3) == 2
    assert result3[0] == {id1, id2, id3}
    assert result3[1] == {id4, id5}