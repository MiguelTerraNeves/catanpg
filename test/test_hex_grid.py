from catanpg.hex_grid import (
    Direction,
    corner_at_distance,
    direction_to_angle,
    distance,
    index_radius,
    move_from_hex,
    next_clockwise_direction,
    next_counter_clockwise_direction,
    rotate_direction,
    step_from_hex,
)


def test_direction_to_angle() -> None:
    assert direction_to_angle(Direction.EAST) == 0
    assert direction_to_angle(Direction.NORTHEAST) == 60
    assert direction_to_angle(Direction.NORTHWEST) == 120
    assert direction_to_angle(Direction.WEST) == 180
    assert direction_to_angle(Direction.SOUTHWEST) == 240
    assert direction_to_angle(Direction.SOUTHEAST) == 300


def test_move_from_hex() -> None:
    assert move_from_hex(0, 0, Direction.EAST, 2) == (2, 0)
    assert move_from_hex(2, 3, Direction.WEST, 4) == (-2, 3)
    assert move_from_hex(-1, 1, Direction.SOUTHEAST, 3) == (-1, 4)
    assert move_from_hex(-1, -1, Direction.SOUTHWEST, 1) == (-2, 0)
    assert move_from_hex(-1, -1, Direction.NORTHEAST, 5) == (4, -6)
    assert move_from_hex(2, 1, Direction.NORTHWEST, 10) == (2, -9)


def test_step_from_hex() -> None:
    assert step_from_hex(2, 3, Direction.EAST) == (3, 3)
    assert step_from_hex(-1, 1, Direction.WEST) == (-2, 1)
    assert step_from_hex(-1, -1, Direction.SOUTHEAST) == (-1, 0)
    assert step_from_hex(-1, -1, Direction.SOUTHWEST) == (-2, 0)
    assert step_from_hex(2, 1, Direction.NORTHEAST) == (3, 0)
    assert step_from_hex(0, 0, Direction.NORTHWEST) == (0, -1)


def test_corner_at_distance() -> None:
    assert corner_at_distance(Direction.EAST, 4) == (4, 0)
    assert corner_at_distance(Direction.WEST, 3) == (-3, 0)
    assert corner_at_distance(Direction.SOUTHEAST, 1) == (0, 1)
    assert corner_at_distance(Direction.SOUTHWEST, 5) == (-5, 5)
    assert corner_at_distance(Direction.NORTHEAST, 10) == (10, -10)
    assert corner_at_distance(Direction.NORTHWEST, 2) == (0, -2)


def test_distance() -> None:
    assert distance(0, 0, 0, 2) == 2
    assert distance(-2, 4, 1, 1) == 3
    assert distance(-2, 0, 4, -2) == 6
    assert distance(1, 1, 1, 1) == 0


def test_index_radius() -> None:
    assert index_radius(2, 0) == 2
    assert index_radius(2, -2) == 2
    assert index_radius(4, 1) == 5
    assert index_radius(0, 0) == 0


def test_rotata_direction() -> None:
    assert rotate_direction(Direction.NORTHEAST, 0) == Direction.NORTHEAST
    assert rotate_direction(Direction.NORTHEAST, 1) == Direction.EAST
    assert rotate_direction(Direction.NORTHEAST, -1) == Direction.NORTHWEST
    assert rotate_direction(Direction.NORTHEAST, 3) == Direction.SOUTHWEST
    assert rotate_direction(Direction.SOUTHEAST, 6) == Direction.SOUTHEAST
    assert rotate_direction(Direction.EAST, 8) == Direction.SOUTHWEST
    assert rotate_direction(Direction.EAST, -8) == Direction.NORTHWEST


def test_next_clockwise_direction() -> None:
    assert next_clockwise_direction(Direction.EAST) == Direction.SOUTHEAST
    assert next_clockwise_direction(Direction.NORTHEAST) == Direction.EAST


def test_next_counterclockwise_direction() -> None:
    assert next_counter_clockwise_direction(Direction.WEST) == Direction.SOUTHWEST
    assert next_counter_clockwise_direction(Direction.EAST) == Direction.NORTHEAST
