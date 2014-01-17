


(define (problem strips-mprime-l3-f3-s5-v2-c2)
(:domain mprime-strips)
(:objects f0 f1 f2 f3 - fuel
          s0 s1 s2 s3 s4 s5 - space
          l0 l1 l2 - location
          v0 v1 - vehicle
          c0 c1 - cargo)
(:init
(not-equal l0 l1)
(not-equal l0 l2)
(not-equal l1 l0)
(not-equal l1 l2)
(not-equal l2 l0)
(not-equal l2 l1)
(fuel-neighbor f0 f1)
(fuel-neighbor f1 f2)
(fuel-neighbor f2 f3)
(space-neighbor s0 s1)
(space-neighbor s1 s2)
(space-neighbor s2 s3)
(space-neighbor s3 s4)
(space-neighbor s4 s5)
(conn l0 l1)
(conn l1 l0)
(conn l1 l2)
(conn l2 l1)
(conn l2 l0)
(conn l0 l2)
(has-fuel l0 f2)
(has-fuel l1 f2)
(has-fuel l2 f0)
(has-space  v0 s2)
(has-space  v1 s2)
(at v0 l1)
(at v1 l2)
(at c0 l0)
(at c1 l2)
)
(:goal
(and
(at c0 l0)
(at c1 l1)
)
)
)


