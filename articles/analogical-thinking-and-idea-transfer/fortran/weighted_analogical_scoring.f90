! Weighted analogical transfer scoring example.
! Compile: gfortran weighted_analogical_scoring.f90 -o weighted_analogical_scoring
! Run: ./weighted_analogical_scoring

program weighted_analogical_scoring
  implicit none

  real :: structural(3), functional(3), surface(3), adaptation(3), context(3)
  real :: legitimacy(3), dynamic(3), innovation(3), evidence(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"A001", "A005", "A007"/)
  structural = (/0.28, 0.89, 0.82/)
  functional = (/0.46, 0.83, 0.78/)
  surface = (/0.82, 0.22, 0.34/)
  adaptation = (/0.34, 0.86, 0.80/)
  context = (/0.30, 0.84, 0.76/)
  legitimacy = (/0.38, 0.78, 0.82/)
  dynamic = (/0.26, 0.86, 0.84/)
  innovation = (/0.29, 0.88, 0.78/)
  evidence = (/0.36, 0.80, 0.76/)

  do i = 1, 3
     score(i) = 0.20 * structural(i) + 0.16 * functional(i) - &
                0.16 * surface(i) + 0.16 * adaptation(i) + &
                0.12 * context(i) + 0.08 * legitimacy(i) + &
                0.08 * dynamic(i) + 0.12 * innovation(i) + &
                0.08 * evidence(i)
  end do

  print *, "Analogical transfer profile scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_analogical_scoring
