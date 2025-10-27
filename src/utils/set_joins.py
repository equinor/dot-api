import uuid

def join_sets_with_common_elements(sets: list[set[uuid.UUID]]) -> list[set[uuid.UUID]]:
    if not sets:
        return []
    
    # Create a copy to avoid modifying the original
    sets = [set(s) for s in sets]
    
    # Keep merging until no more merges are possible
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(sets):
            j = i + 1
            while j < len(sets):
                # Check if sets i and j have common elements
                if sets[i] & sets[j]:
                    # Merge set j into set i
                    sets[i] |= sets[j]
                    # Remove set j
                    sets.pop(j)
                    changed = True
                    # Don't increment j since we removed an element
                else:
                    j += 1
            i += 1
    
    return sets
