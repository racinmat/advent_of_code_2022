(define (domain valves_problem-domain)
 (:requirements :strips :typing :negative-preconditions :disjunctive-preconditions :equality :fluents)
 (:types Location)
 (:predicates (position ?location - Location) (is_connected ?location_1 - Location ?location_2 - Location))
 (:functions (remaining_time) (total_points) (add_per_round))
 (:action move
  :parameters ( ?l_from - Location ?l_to - Location)
  :precondition (and (<= 1 (remaining_time)) (position ?l_from) (not (position ?l_to)) (or (is_connected ?l_from ?l_to) (is_connected ?l_to ?l_from)))
  :effect (and (not (position ?l_from)) (position ?l_to) (assign (remaining_time) (- (remaining_time) 1)) (assign (total_points) (+ (add_per_round) (total_points)))))
 (:action open_valve
  :parameters ( ?at - Location)
  :precondition (and (<= 1 (remaining_time)) (position ?at) (not (valve_open ?at)))
  :effect (and (assign (remaining_time) (- (remaining_time) 1)) (assign (add_per_round) (+ (flow_rate ?at) (total_points))) (assign (total_points) (+ (add_per_round) (total_points)))))
)
