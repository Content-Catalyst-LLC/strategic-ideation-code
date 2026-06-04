! Weighted problem-framing scoring example.
! Compile: gfortran weighted_framing_scoring.f90 -o weighted_framing_scoring
! Run: ./weighted_framing_scoring

program weighted_framing_scoring
  implicit none

  real :: boundary(3), stakeholder(3), systems(3), causal(3), assumptions(3)
  real :: reframing(3), actionability(3), lock_in(3), politics(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"F001", "F003", "F005"/)
  boundary = (/0.28, 0.86, 0.82/)
  stakeholder = (/0.34, 0.79, 0.92/)
  systems = (/0.26, 0.91, 0.78/)
  causal = (/0.31, 0.84, 0.74/)
  assumptions = (/0.24, 0.78, 0.76/)
  reframing = (/0.22, 0.82, 0.80/)
  actionability = (/0.62, 0.72, 0.74/)
  lock_in = (/0.82, 0.32, 0.34/)
  politics = (/0.70, 0.34, 0.30/)

  do i = 1, 3
     score(i) = 0.16 * boundary(i) + 0.15 * stakeholder(i) + &
                0.15 * systems(i) + 0.16 * causal(i) + &
                0.12 * assumptions(i) + 0.13 * reframing(i) + &
                0.11 * actionability(i) - 0.10 * lock_in(i) - &
                0.08 * politics(i)
  end do

  print *, "Problem-framing scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_framing_scoring
