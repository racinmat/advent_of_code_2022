(define (problem valves_problem-problem)
 (:domain valves_problem-domain)
 (:objects 
   AA BB CC DD EE FF GG HH II JJ - Location
 )
 (:init (position AA) (= (flow_rate AA) 0) (= (flow_rate BB) 13) (= (flow_rate CC) 2) (= (flow_rate DD) 20) (= (flow_rate EE) 3) (= (flow_rate FF) 0) (= (flow_rate GG) 0) (= (flow_rate HH) 22) (= (flow_rate II) 0) (= (flow_rate JJ) 21) (is_connected AA BB) (is_connected AA DD) (is_connected AA II) (is_connected BB AA) (is_connected BB CC) (is_connected CC BB) (is_connected CC DD) (is_connected DD AA) (is_connected DD CC) (is_connected DD EE) (is_connected EE DD) (is_connected EE FF) (is_connected FF EE) (is_connected FF GG) (is_connected GG FF) (is_connected GG HH) (is_connected HH GG) (is_connected II AA) (is_connected II JJ) (is_connected JJ II) (= (total_points) 0) (= (remaining_time) 30))
 (:goal (and (= (remaining_time) 0)))
 (:metric maximize (total_points))
)
