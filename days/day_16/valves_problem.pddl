(define (problem valves_problem-problem)
 (:domain valves_problem-domain)
 (:objects 
   AA BB CC DD EE FF GG HH II JJ - Location
 )
 (:init (position AA) (valve_closed AA) (= (flow_rate AA) 0) (valve_closed BB) (= (flow_rate BB) 13) (valve_closed CC) (= (flow_rate CC) 2) (valve_closed DD) (= (flow_rate DD) 20) (valve_closed EE) (= (flow_rate EE) 3) (valve_closed FF) (= (flow_rate FF) 0) (valve_closed GG) (= (flow_rate GG) 0) (valve_closed HH) (= (flow_rate HH) 22) (valve_closed II) (= (flow_rate II) 0) (valve_closed JJ) (= (flow_rate JJ) 21) (is_connected AA BB) (is_connected AA DD) (is_connected AA II) (is_connected BB AA) (is_connected BB CC) (is_connected CC BB) (is_connected CC DD) (is_connected DD AA) (is_connected DD CC) (is_connected DD EE) (is_connected EE DD) (is_connected EE FF) (is_connected FF EE) (is_connected FF GG) (is_connected GG FF) (is_connected GG HH) (is_connected HH GG) (is_connected II AA) (is_connected II JJ) (is_connected JJ II) (= (total_points) 0) (= (remaining_time) 30))
 (:goal (and (= (remaining_time) 0)))
 (:metric maximize (total_points))
)
