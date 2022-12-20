(define (domain valves_problem-domain)
 (:requirements :strips :typing :equality :fluents)
 (:types Location)
 (:predicates (position ?location - Location) (is_connected ?location_1 - Location ?location_2 - Location) (valve_closed ?location - Location))
 (:functions (remaining_time) (total_points) (flow_rate ?location - Location))
 (:action move
  :parameters ( ?l_from - Location ?l_to - Location)
  :precondition (and (< 0 (remaining_time)) (position ?l_from) (is_connected ?l_from ?l_to))
  :effect (and (not (position ?l_from)) (position ?l_to) (decrease (remaining_time) 1)))
 (:action open_valve
  :parameters ( ?at - Location)
  :precondition (and (< 0 (remaining_time)) (position ?at) (valve_closed ?at))
  :effect (and (decrease (remaining_time) 1) (increase (total_points) (* (remaining_time) (flow_rate ?at))) (not (valve_closed ?at))))
)
