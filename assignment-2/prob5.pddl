


(define (problem strips-mprime-l5-f5-s5-v2-c3)
(:domain mprime-strips)
(:objects f0 f1 f2 f3 f4 f5 - fuel
          s0 s1 s2 s3 s4 s5 - space
          l0 l1 l2 l3 l4 - location
          v0 v1 - vehicle
          c0 c1 c2 - cargo)
(:init
(not-equal l0 l1)
(not-equal l0 l2)
(not-equal l0 l3)
(not-equal l0 l4)
(not-equal l1 l0)
(not-equal l1 l2)
(not-equal l1 l3)
(not-equal l1 l4)
(not-equal l2 l0)
(not-equal l2 l1)
(not-equal l2 l3)
(not-equal l2 l4)
(not-equal l3 l0)
(not-equal l3 l1)
(not-equal l3 l2)
(not-equal l3 l4)
(not-equal l4 l0)
(not-equal l4 l1)
(not-equal l4 l2)
(not-equal l4 l3)
(fuel-neighbor f0 f1)
(fuel-neighbor f1 f2)
(fuel-neighbor f2 f3)
(fuel-neighbor f3 f4)
(fuel-neighbor f4 f5)
(space-neighbor s0 s1)
(space-neighbor s1 s2)
(space-neighbor s2 s3)
(space-neighbor s3 s4)
(space-neighbor s4 s5)
(conn l0 l1)
(conn l1 l0)
(conn l1 l2)
(conn l2 l1)
(conn l2 l3)
(conn l3 l2)
(conn l3 l4)
(conn l4 l3)
(conn l4 l0)
(conn l0 l4)
(has-fuel l0 f5)
(has-fuel l1 f4)
(has-fuel l2 f3)
(has-fuel l3 f1)
(has-fuel l4 f3)
(has-space  v0 s1)
(has-space  v1 s5)
(at v0 l0)
(at v1 l2)
(at c0 l0)
(at c1 l2)
(at c2 l1)
)
(:goal
(and
(at c0 l0)
(at c1 l1)
(at c2 l4)
)
)
)


