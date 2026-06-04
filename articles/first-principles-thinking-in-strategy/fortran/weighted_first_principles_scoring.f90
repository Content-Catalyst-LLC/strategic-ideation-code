program weighted_first_principles_scoring
  implicit none
  real :: assumptions(2), clarity(2), constraints(2), reconstruction(2), adaptation(2), score(2)
  character(len=5) :: ids(2)
  integer :: i
  ids=(/"FP001","FP003"/); assumptions=(/0.84,0.22/); clarity=(/0.31,0.88/); constraints=(/0.28,0.91/); reconstruction=(/0.34,0.89/); adaptation=(/0.39,0.92/)
  do i=1,2
    score(i)=-0.16*assumptions(i)+0.18*clarity(i)+0.18*constraints(i)+0.18*reconstruction(i)+0.14*adaptation(i)
    print *, trim(ids(i)), score(i)
  end do
end program weighted_first_principles_scoring
