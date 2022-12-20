(define (domain valves_problem-domain)
 (:requirements :strips :typing :negative-preconditions :disjunctive-preconditions :equality :fluents)
 (:types Location)
 (:predicates (position ?location - Location) (is_connected ?location_1 - Location ?location_2 - Location) (valve_open ?location - Location))
 (:functions (remaining_time) (total_points) (flow_rate ?location - Location))
 (:action move
  :parameters ( ?l_from - Location ?l_to - Location)
  :precondition (and (< 0 (remaining_time)) (position ?l_from) (not (position ?l_to)) (or (is_connected ?l_from ?l_to) (is_connected ?l_to ?l_from)))
  :effect (and (not (position ?l_from)) (position ?l_to) (decrease (remaining_time) 1)))
 (:action open_valve
  :parameters ( ?at - Location)
  :precondition (and (< 0 (remaining_time)) (position ?at) (not (valve_open ?at)))
  :effect (and (decrease (remaining_time) 1) (increase (total_points) (* (remaining_time) (flow_rate ?at))) (valve_open ?at)))
)
